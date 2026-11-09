+++
id = "pipelines.idempotency-and-reruns"
title = "Idempotency and safe reruns"
minutes = 30
+++

# Idempotency and safe reruns

Every pipeline gets run twice. Someone retries a failed job, a scheduler fires a duplicate, you backfill last week. If running twice gives a different result from running once, you have a bug that will surface at 3 a.m.

> **dbt bridge.** A `table` materialization is idempotent: it rebuilds from scratch and the result depends only on the inputs. An `incremental` model with `unique_key` is idempotent through `merge`. An incremental model with no `unique_key` just inserts, and a rerun duplicates rows. You already know this failure; now you will build the safeguards yourself.

**Idempotent** means: running the operation N times leaves the same state as running it once.

## Three ways to write rows

> **Predict first.** You load the same two rows into a table three times. Which strategy leaves 2 rows, and which leaves 6?

```python
def append(table, rows):
    table.extend(rows)

def overwrite(table, rows):
    table[:] = rows

def upsert(table, rows, key):
    by_key = {r[key]: r for r in table}
    for r in rows:
        by_key[r[key]] = r
    table[:] = by_key.values()

batch = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}]
for name, fn in [("append", lambda t: append(t, batch)),
                 ("overwrite", lambda t: overwrite(t, batch)),
                 ("upsert", lambda t: upsert(t, batch, "id"))]:
    table = []
    for _ in range(3):
        fn(table)
    print(name, len(table))
```

Append is not idempotent. Overwrite is, but it replaces everything, which is wrong if the batch only covers one day. Upsert is idempotent and surgical, but needs a reliable key.

## Partition replace: delete then insert

The workhorse for date-partitioned fact tables is: delete the slice you are about to write, insert it, all in **one transaction**. The warehouse analogue is `DELETE ... WHERE load_date = ...` followed by `INSERT`, or `INSERT OVERWRITE`.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("create table fact (load_date text, order_id int, amount real)")

def load_partition(conn, load_date, rows):
    with conn:  # one transaction: commit on success, rollback on error
        conn.execute("delete from fact where load_date = ?", (load_date,))
        conn.executemany(
            "insert into fact values (?, ?, ?)",
            [(load_date, oid, amt) for oid, amt in rows],
        )

load_partition(conn, "2026-01-01", [(1, 10.0), (2, 5.0)])
load_partition(conn, "2026-01-01", [(1, 10.0), (2, 5.0)])  # rerun
load_partition(conn, "2026-01-02", [(3, 7.5)])
print(conn.execute("select load_date, count(*) from fact group by 1 order by 1").fetchall())
```

Without the transaction, a crash between delete and insert would leave a hole. The `with conn:` block makes both steps succeed or neither.

## Run ids and logical dates

Separate **when the job ran** from **which data it is for**. The *logical date* (the partition) is an input; rerunning for the same logical date must give the same output. Never compute the partition from `datetime.now()` inside the transform.

```python
import hashlib

def run_id(pipeline: str, logical_date: str, attempt: int = 1) -> str:
    raw = f"{pipeline}|{logical_date}|{attempt}"
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

print(run_id("orders", "2026-01-01"))
print(run_id("orders", "2026-01-01"))          # same inputs, same id
print(run_id("orders", "2026-01-01", attempt=2))
```

Stamp every row you write with a run id (or `_loaded_at` plus run id). When a bad run needs cleaning, `delete where _run_id = ...` is trivial.

## Deterministic outputs

A rerun should produce byte-identical files. Common leaks of nondeterminism:

- iterating a `set` (order can vary between runs) or relying on unordered query results: sort explicitly
- `datetime.now()` or `uuid4()` inside transforms
- random sampling without a seed

```python
rows = [{"id": 3}, {"id": 1}, {"id": 2}]
ordered = sorted(rows, key=lambda r: r["id"])
print(ordered)
```

## Atomic writes: temp file then rename

If a job dies while writing `daily.csv`, downstream readers see a truncated file. Fix: write to a temp file in the **same directory**, then `os.replace` it over the target. A rename on one filesystem is atomic: readers see the old file or the new file, never half of one.

```python
import os, tempfile
from pathlib import Path

def atomic_write_text(path, text):
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise

with tempfile.TemporaryDirectory() as d:
    target = Path(d) / "daily.csv"
    atomic_write_text(target, "a,b\n1,2\n")
    atomic_write_text(target, "a,b\n3,4\n")
    print(target.read_text(), sorted(p.name for p in Path(d).iterdir()))
```

The temp file must be in the same directory: renaming across filesystems is a copy, which is not atomic.

## Common mistakes

- Using `INSERT` for a rerunnable job and then "fixing" duplicates with a dedupe query downstream.
- Delete and insert as two separate commits.
- Writing the temp file in `/tmp` and renaming into a different mount: `OSError: [Errno 18] Invalid cross-device link`.
- Deriving the partition from the wall clock, so a backfill writes today's date.

## What to take away

1. Idempotent means N runs equal one run.
2. Append is the unsafe default; prefer overwrite-a-partition or upsert on a key.
3. Wrap delete plus insert in one transaction.
4. Treat the logical date as an input and stamp rows with a run id.
5. Write files to a temp path in the same directory, then `os.replace`.
