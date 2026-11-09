+++
id = "capstones.capstone-elt-pipeline"
title = "Capstone: an ELT pipeline"
minutes = 90
+++

# Capstone: an ELT pipeline

This is the first of three capstones. There is no new syntax here. You will combine validation, pure transforms, idempotent loading, incremental processing, logging and a CLI into one pipeline you could hand to a teammate and run on a schedule.

> **SQL bridge.** You have built this in dbt: a staging layer that cleans, a mart that aggregates, incremental models keyed by a watermark, tests that quarantine bad data. Here you build the same layers in Python, with each layer in its own file so you can test it alone.

## The brief

The shop exports three CSV files: `orders.csv`, `order_items.csv` and `customers.csv`. Build a command-line pipeline that:

1. **Extracts** the three files.
2. **Validates** every row against a schema; bad rows are **quarantined** (kept, with the reason), never silently dropped and never allowed to crash the run.
3. **Transforms** valid rows into a `daily_revenue` table: one row per `(day, region)` with order count and revenue, counting only `completed` and `shipped` orders.
4. **Loads** into sqlite so that running it twice gives the same result (**idempotent**).
5. Supports **incremental** runs driven by a **watermark**, so a daily schedule does not rebuild history.
6. **Logs** what it did and exits with a meaningful code.

## Architecture

```text
pipeline/
  schema.py     validate_*  : raw dict rows -> (good typed rows, quarantined rows)     pure
  transform.py  daily_revenue: good rows -> aggregate rows                              pure
  load.py       sqlite: tables, idempotent load, quarantine, watermark                  I/O
  run.py        read CSVs, call the layers in order, return stats                       orchestration
  cli.py        argparse + exit codes                                                   edge
```

Dependencies point one way: `cli -> run -> (schema, transform, load)`. Pure functions know nothing about files or databases, which is why their tests need no setup.

## Design decisions to think through

**Validate at the edge, then trust.** Every value in a CSV is text. Convert and check once, in `schema.py`. After that, `transform.py` can assume `quantity` is an `int`. A validator that returns `(good, bad)` instead of raising keeps one bad row from killing a million good ones:

```python
def split_rows(rows, check):
    good, bad = [], []
    for row in rows:
        try:
            good.append(check(row))
        except ValueError as exc:
            bad.append({"reason": str(exc), "raw": row})
    return good, bad

def positive_int(row):
    value = int(row["qty"])             # ValueError if not a number
    if value < 1:
        raise ValueError("qty must be a positive integer")
    return {"qty": value}

good, bad = split_rows([{"qty": "3"}, {"qty": "x"}, {"qty": "0"}], positive_int)
print(good)
print([b["reason"] for b in bad])
```

**Idempotency by replacing partitions.** Appending on every run duplicates data. Instead, delete the days you are about to write and insert the new rows, inside **one transaction** so readers never see half a day:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("create table daily(day text, total real)")

def load_days(conn, rows):
    with conn:                                        # commit on success, roll back on error
        conn.executemany("delete from daily where day = ?", [(d,) for d in {r[0] for r in rows}])
        conn.executemany("insert into daily values (?, ?)", rows)

load_days(conn, [("2025-01-01", 10.0), ("2025-01-02", 20.0)])
load_days(conn, [("2025-01-01", 10.0), ("2025-01-02", 20.0)])     # run it again
print(conn.execute("select * from daily order by day").fetchall())
```

> **Predict first.** Run twice, how many rows? Two. The delete makes the second run a no-op rather than a duplicate.

**The watermark and late data.** An incremental run remembers the latest day it loaded and next time only looks at newer data. But data arrives late: an order placed on the 2nd may show up in the file on the 3rd. If you start strictly *after* the watermark you lose it forever. The pragmatic rule used here: reprocess from the watermark day **inclusive**. Because loading replaces whole days, the overlap is harmless. (Late arrivals older than the watermark day need a wider lookback window; know the limit of your design.)

**Quarantine, don't drop.** Dropped rows are invisible and you cannot ask "why is revenue 2% lower than finance's number?". Store the raw row and the reason. Make saving idempotent with a key derived from the row content, so re-running does not pile up duplicates.

**Order of side effects.** Read every input *before* creating or touching the database. If a file is missing you want a clean failure with nothing half-written.

**Logging, not printing.** Library code uses `logging.getLogger("pipeline")`. INFO for progress, WARNING when something was quarantined. The CLI decides how logging is configured and what exit code to return: `0` success, `2` missing input.

## A tiny CLI with `argparse`

```python
import argparse

def build_parser():
    p = argparse.ArgumentParser(prog="pipeline")
    p.add_argument("--data-dir", required=True)
    p.add_argument("--incremental", action="store_true")
    return p

args = build_parser().parse_args(["--data-dir", "exports", "--incremental"])
print(args.data_dir, args.incremental)
```

`main(argv=None)` takes the argument list as a parameter instead of reading `sys.argv` directly. That one habit makes a CLI testable.

## How to work

1. Read the prompt's contract table for `schema.py`; make `test_schema` pass.
2. `transform.py` next: pure, easy, and the tests tell you the exact edge cases.
3. `load.py`: transactions, partition replace, quarantine key, watermark.
4. `run.py` and `cli.py` last; by then most of the logic is done.
5. Run **Check** after every file. Failing tests name the behavior that is missing.

## Common mistakes

- **Appending instead of replacing**, then wondering why totals double after a re-run.
- **`int(value)` outside a `try`**: one bad row raises `ValueError: invalid literal for int() with base 10: 'abc'` and the whole run dies.
- **Strict `>` against the watermark**, which silently drops same-day late rows.
- **Opening the database before reading inputs**, leaving an empty file behind on failure.
- **Mutating the input rows** while cleaning them; copy, don't edit in place.
- **`print` in library code**, which cannot be silenced or routed.

## What to take away

1. Layer the pipeline: pure validation and transforms, then I/O, then orchestration, then the CLI.
2. Validators return `(good, quarantined)`; reasons name the field.
3. Idempotent loads replace partitions inside one transaction.
4. A watermark with an inclusive lookback tolerates late data.
5. Quarantine, log and exit codes make a pipeline operable, not just correct.
