+++
id = "performance-and-concurrency.memory-and-streaming"
title = "Memory and streaming"
minutes = 30
+++

# Memory and streaming

Your laptop has 16 GB. A month of events is 40 GB. The first time a script dies with `MemoryError` (or the machine starts swapping and everything crawls), you learn the central idea of this lesson: **don't hold the whole dataset; flow it through.**

> **SQL bridge.** A warehouse never loads a table into memory to answer `SUM(...)`; it scans micro-partitions and keeps a running total. A Python **generator** is the same pattern: produce one row, use it, forget it. And Polars' lazy mode is a query optimiser for your DataFrames, like Snowflake planning before it executes.

## Lists versus generators

A list holds every element at once. A generator produces elements **on demand**.

```python
import sys

as_list = [n * n for n in range(1_000_000)]
as_gen = (n * n for n in range(1_000_000))
print(sys.getsizeof(as_list) > 1_000_000, sys.getsizeof(as_gen) < 1_000)
print(sum(as_gen))
```

The list comprehension (square brackets) builds a million numbers. The generator expression (parentheses) holds only its recipe and current position. A generator can be consumed **once**:

```python
gen = (n for n in range(3))
print(list(gen))
print(list(gen))      # already exhausted
```

> **Predict first.** What does the second `print` show? An empty list, `[]`: the generator is spent. This surprises people who pass a generator to two functions in a row.

## Writing a generator function

Use `yield` instead of `return`. Each `yield` pauses the function and hands back one value; the function resumes where it left off.

```python
import csv
import os
from pathlib import Path

def read_rows(path):
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            yield row                 # one row at a time; the file is never fully in memory

orders_csv = Path(os.environ["DOJO_DATA"]) / "orders.csv"
shipped = sum(1 for row in read_rows(orders_csv) if row["status"] == "shipped")
print(shipped)
```

Memory stays flat whether the file has 1,500 rows or 150 million. Generators also **compose**: feed one into another and the data streams through the whole chain without ever being materialised.

```python
import csv
import os
from pathlib import Path

def read_rows(path):
    with open(path, newline="") as f:
        yield from csv.DictReader(f)

orders_csv = Path(os.environ["DOJO_DATA"]) / "orders.csv"

def only_status(rows, status):
    return (r for r in rows if r["status"] == status)

def take(n, rows):
    for i, row in enumerate(rows):
        if i >= n:
            return
        yield row

first_two = list(take(2, only_status(read_rows(orders_csv), "refunded")))
print([r["order_id"] for r in first_two])
```

`take` stops pulling after two matches, so the rest of the file is never even read.

## Chunked processing

Row-at-a-time is memory-perfect but slow for work that is cheaper in bulk (database inserts, writing files). The middle ground is **chunks**: read, say, 500 rows at a time.

```python
from itertools import islice

def chunks(iterable, size):
    it = iter(iterable)
    while batch := list(islice(it, size)):
        yield batch

sizes = [len(b) for b in chunks(range(10), 4)]
print(sizes)
```

`islice(it, size)` takes up to `size` items from the shared iterator; when it returns nothing, the loop ends. (Python 3.12 also ships `itertools.batched`, which does the same job, yielding tuples.)

## Batching writes

One insert per row means one round trip per row, which is painfully slow against a real warehouse. One giant insert means holding everything in memory. Batch:

```python
import sqlite3
from itertools import islice

def chunks(iterable, size):
    it = iter(iterable)
    while batch := list(islice(it, size)):
        yield batch

conn = sqlite3.connect(":memory:")
conn.execute("create table events(id integer, kind text)")

def load(conn, rows, batch_size=3):
    total = 0
    for batch in chunks(rows, batch_size):
        conn.executemany("insert into events values (?, ?)", batch)
        conn.commit()                    # each batch is durable on its own
        total += len(batch)
    return total

stream = ((i, "click") for i in range(10))   # a generator: never fully in memory
print(load(conn, stream), conn.execute("select count(*) from events").fetchone()[0])
```

The generator streams in, `chunks` groups, `executemany` writes. At no point does more than one batch exist in memory.

## Polars: eager versus lazy

`pl.read_csv` is **eager**: it loads the whole file now. `pl.scan_csv` is **lazy**: it returns a `LazyFrame`, a *plan*. Nothing is read until you call `.collect()`, and the optimiser can then read only the needed columns and push filters down to the file scan.

```python
import os
from pathlib import Path

import polars as pl

orders_csv = Path(os.environ["DOJO_DATA"]) / "orders.csv"

lazy = (
    pl.scan_csv(orders_csv)
    .filter(pl.col("status") == "shipped")
    .group_by("customer_id")
    .agg(pl.len().alias("shipped_orders"))
    .sort(["shipped_orders", "customer_id"], descending=[True, False])
    .head(3)
)
print(type(lazy).__name__)        # still just a plan
print(lazy.collect())             # now it runs
```

Use eager for exploring a small file interactively. Use lazy in pipelines: it reads less, uses less memory, and returns the plan so callers can add steps before executing.

## Common mistakes

- **`list(generator)` "just to look".** It defeats the whole point and may blow memory.
- **Reusing a spent generator.** Second pass is silently empty. Re-create it or return a list when you need two passes.
- **Reading the whole file with `.read()` or `readlines()`.** Iterate over the file object instead.
- **Collecting too early in Polars.** Calling `.collect()` in the middle of a pipeline and continuing eagerly throws away the optimiser.
- **Committing per row.** One commit per row is the slowest possible write pattern; commit per batch.

## What to take away

1. Generators (`yield`, or parenthesised expressions) produce values on demand and use constant memory.
2. A generator is single-use; compose them to stream data through a pipeline.
3. Chunk when bulk operations are cheaper than row-by-row: `islice` in a loop does it.
4. Batch writes: `executemany` plus one commit per batch.
5. `scan_csv` plus `.collect()` last: lazy plans read less and use less memory than eager loading.
