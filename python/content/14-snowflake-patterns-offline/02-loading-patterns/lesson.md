+++
id = "snowflake-patterns-offline.loading-patterns"
title = "Loading patterns"
minutes = 30
+++

# Loading patterns

Getting data **into** Snowflake from Python is where beginners write a loop of single-row `INSERT`s and wait an hour. You know the warehouse likes big, set-based, file-based loads. This lesson maps that knowledge to Python code, and everything here is simulated offline.

> **Snowflake bridge.** The fast path is `PUT file @stage` then `COPY INTO table FROM @stage`. Python's job is to *produce good files*, *batch* what it sends, and make reruns **idempotent**, i.e. `MERGE`, not blind `INSERT`.

## Options and tradeoffs

| Approach | Good for | Weakness |
|---|---|---|
| `INSERT` one row at a time | demos, tiny control tables | one round trip per row; very slow |
| `executemany` batches | thousands of rows | still row-oriented SQL; size limits |
| stage a file + `COPY INTO` | anything big; the default | needs a file and a stage |
| `write_pandas`-style helper | a DataFrame already in memory | writes Parquet to a temp stage and runs `COPY INTO` for you; memory-bound |
| `MERGE` from a staging table | reruns, upserts, late data | needs a business key |

`write_pandas` is not magic: it serialises the frame to Parquet files, uploads them to a temporary stage, then issues `COPY INTO`. If you understand that, you understand why it is fast and why a 50 GB frame is still a bad idea.

## Batching rows

Turning any iterable into fixed-size lists is a tiny generator you will write many times:

```python
from collections.abc import Iterable, Iterator
from itertools import islice

def batched(items: Iterable, size: int) -> Iterator[list]:
    if size < 1:
        raise ValueError("size must be >= 1")
    it = iter(items)
    while chunk := list(islice(it, size)):
        yield chunk

print(list(batched(range(7), 3)))
```

Because it is a generator, a 10 million row file streams through with only `size` rows in memory.

## Sending a batch: one transaction, not many

```python
import sqlite3

def load(conn, rows, batch_size=2):
    cur = conn.cursor()
    try:
        for chunk in batched(rows, batch_size):
            cur.executemany("INSERT INTO orders (id, amount) VALUES (?, ?)", chunk)
        conn.commit()
    except Exception:
        conn.rollback()
        raise

def batched(items, size):
    from itertools import islice
    it = iter(items)
    while chunk := list(islice(it, size)):
        yield chunk

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, amount REAL)")
load(conn, [(1, 9.5), (2, 20.0), (3, 7.25)])
print(conn.execute("SELECT COUNT(*), SUM(amount) FROM orders").fetchone())
try:
    load(conn, [(4, 1.0), (4, 2.0)])      # duplicate key fails mid-way
except sqlite3.IntegrityError as e:
    print("failed:", e)
print(conn.execute("SELECT COUNT(*) FROM orders").fetchone())
```

> **Predict first.** The second `load` fails on its last row. Is row `(4, 1.0)` in the table afterwards?

No: the rollback removed the whole attempt. All-or-nothing is what lets you safely re-run a job.

## Chunking big files

`COPY INTO` likes many moderately sized files (think 100-250 MB compressed) so it can load them in parallel. One giant file loads on one thread. Split by **row count** while streaming, so memory stays flat:

```python
import csv
import io

def split_csv(rows, header, max_rows):
    """Yield CSV text chunks, each with the header."""
    chunk, n = [], 0
    for row in rows:
        chunk.append(row)
        if len(chunk) == max_rows:
            yield render(header, chunk)
            chunk = []
    if chunk:
        yield render(header, chunk)

def render(header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    return buf.getvalue()

parts = list(split_csv([(i, i * 10) for i in range(5)], ["id", "amount"], 2))
print(len(parts))
print(parts[-1])
```

## Idempotent loads: MERGE from a spec

Run the job twice and the table must look the same as running it once. The pattern: load to a **staging** table (cheap, disposable), then `MERGE` into the target on the business key. Generating that SQL from a description of the table removes copy-paste mistakes across dozens of tables.

```python
def build_merge(table: str, staging: str, keys: list[str], columns: list[str]) -> str:
    on = " AND ".join(f"tgt.{k} = src.{k}" for k in keys)
    updates = ", ".join(f"tgt.{c} = src.{c}" for c in columns if c not in keys)
    cols = ", ".join(columns)
    vals = ", ".join(f"src.{c}" for c in columns)
    return (
        f"MERGE INTO {table} AS tgt USING {staging} AS src ON {on} "
        f"WHEN MATCHED THEN UPDATE SET {updates} "
        f"WHEN NOT MATCHED THEN INSERT ({cols}) VALUES ({vals})"
    )

print(build_merge("orders", "orders_stg", ["order_id"], ["order_id", "status", "amount"]))
```

Think about late-arriving data: if a source row can be corrected tomorrow, `MERGE` updates it; a plain `INSERT` would duplicate it. Also dedupe the staging data first: `MERGE` errors or behaves non-deterministically when several source rows match one target row.

## The whole shape of a job

```python
# no-run
def run(conn, source_rows):
    with conn.cursor() as cur:
        cur.execute("CREATE TEMPORARY TABLE orders_stg LIKE orders")
        # PUT chunks to a stage, COPY INTO orders_stg ...
        cur.execute(build_merge("orders", "orders_stg", ["order_id"], COLUMNS))
```

Staging tables are `TEMPORARY` so a crash leaves nothing behind.

## Common mistakes

- Row-by-row `INSERT` in a Python loop: 100k rows, 100k round trips.
- Committing per batch and failing halfway: the table now holds a partial load that a re-run duplicates.
- `list(rows)` on a huge generator, loading everything into memory before batching.
- A load keyed on nothing: reruns append duplicates. Pick a business key.
- `MERGE` with duplicate keys in the source: `Duplicate row detected during DML action`. Dedupe first.
- One 20 GB file instead of many mid-sized ones.

## What to take away

1. Big loads are files plus `COPY INTO`; `INSERT` loops are for tiny data.
2. `write_pandas`-style helpers are stage-and-copy under the hood.
3. Stream with generators; batch with a small `batched` helper.
4. One transaction per load, rollback on failure.
5. Make loads idempotent: stage, dedupe, `MERGE` on a business key, generated from a spec.
