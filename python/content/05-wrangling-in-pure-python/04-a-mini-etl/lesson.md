+++
id = "wrangling-in-pure-python.a-mini-etl"
title = "A mini ETL"
minutes = 35
+++

# A mini ETL

This lesson assembles the module: files, errors, logging, cleaning and aggregation become one small pipeline that is safe to re-run. It is the shape of every production job you will write, whether the destination is sqlite today or Snowflake tomorrow.

> **SQL bridge.** In dbt terms: `raw` source → staging model (cast, clean, filter bad rows) → mart (aggregate) → table. The extra production concerns are what happens to the bad rows, and what happens when the job runs twice.

## The shape

```
extract  ->  validate  ->  transform  ->  load
  file       good / bad     aggregate     table (idempotent)
                |
                +--> rejects file (with reasons)
```

Design rules:

1. **Each stage is a small function** that takes data and returns data. Only extract and load touch the outside world.
2. **Bad rows are data too.** They go to a rejects file with a line number and a reason, never into the void.
3. **Load is idempotent.** Running the job twice must give the same table, not double.
4. **Counts reconcile.** `read == loaded + rejected`, and you log it.

## Extract and validate

Raw input, as a CSV of order lines:

```python
import csv
import io
from decimal import Decimal

RAW = """order_id,customer_id,sku,quantity,unit_price
A1,1,x-100,2,5.00
A1,1,y-200,1,12.50
A2,2,x-100,0,5.00
A3,two,z-300,1,1.00
A4,2,y-200,3,12.50
"""

def validate(raw):
    errors = []
    try:
        customer_id = int(raw["customer_id"])
    except ValueError:
        errors.append("customer_id must be an integer")
    try:
        quantity = int(raw["quantity"])
        if quantity <= 0:
            errors.append("quantity must be positive")
    except ValueError:
        errors.append("quantity must be an integer")
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "order_id": raw["order_id"],
        "customer_id": customer_id,
        "sku": raw["sku"].upper(),
        "quantity": quantity,
        "unit_price": Decimal(raw["unit_price"]),
    }

valid, rejects = [], []
for line_no, raw in enumerate(csv.DictReader(io.StringIO(RAW)), start=2):   # header is line 1
    try:
        valid.append(validate(raw))
    except ValueError as e:
        rejects.append({"line": line_no, "reason": str(e)})

print(len(valid), "valid;", rejects)
```

`start=2` makes the reported number match what someone sees when they open the file in an editor. Small details like this decide whether a rejects file is usable.

## Transform

A pure function from clean rows to the output shape. Easy to test because it needs no files.

```python
from decimal import Decimal

def customer_totals(valid):
    out = {}
    for r in valid:
        t = out.setdefault(r["customer_id"], {"customer_id": r["customer_id"], "line_count": 0, "revenue": Decimal("0")})
        t["line_count"] += 1
        t["revenue"] += r["quantity"] * r["unit_price"]
    return [out[k] for k in sorted(out)]

valid = [
    {"customer_id": 1, "quantity": 2, "unit_price": Decimal("5.00")},
    {"customer_id": 1, "quantity": 1, "unit_price": Decimal("12.50")},
    {"customer_id": 2, "quantity": 3, "unit_price": Decimal("12.50")},
]
for t in customer_totals(valid):
    print(t)
```

## Load, idempotently

The trick for a re-runnable load is to make the write a **replace by key**, the same idea as `MERGE` or "delete then insert for this batch". With sqlite that is `INSERT OR REPLACE` on a `PRIMARY KEY`.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE IF NOT EXISTS order_lines (
        order_id TEXT, sku TEXT, quantity INTEGER, unit_price TEXT,
        PRIMARY KEY (order_id, sku)
    )
""")

rows = [("A1", "X-100", 2, "5.00"), ("A1", "Y-200", 1, "12.50")]

def load(conn, rows):
    with conn:                                 # one transaction: all or nothing
        conn.executemany("INSERT OR REPLACE INTO order_lines VALUES (?, ?, ?, ?)", rows)

load(conn, rows)
load(conn, rows)                               # second run: no duplicates
print(conn.execute("SELECT COUNT(*) FROM order_lines").fetchone()[0])
```

Two habits are visible here. `with conn:` wraps the writes in a transaction that commits on success and rolls back on an exception, so a crash cannot leave a half-loaded table. And the `?` placeholders pass values separately from the SQL text. **Never** build SQL with f-strings from data; that is how injection and quoting bugs happen.

Store money as text (or integer cents) in sqlite, which has no exact decimal type; convert back with `Decimal(text)` when reading.

## The rejects file

```python
import csv
import io

rejects = [{"line": 4, "reason": "quantity must be positive"}, {"line": 5, "reason": "customer_id must be an integer"}]

buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=["line", "reason"], lineterminator="\n")
w.writeheader()
w.writerows(rejects)
print(buf.getvalue())
```

Write the file **even when it is empty** (header only). "No rejects file" is ambiguous: did the job find none, or fail before getting there?

## Wire it together and report

```python
import logging

log = logging.getLogger("etl")

def run(read_rows, load_rows, write_rejects):
    valid, rejects = [], []
    for n, raw in read_rows():
        try:
            valid.append(validate_one(raw))
        except ValueError as e:
            rejects.append({"line": n, "reason": str(e)})
    load_rows(valid)
    write_rejects(rejects)
    log.info("read=%d loaded=%d rejected=%d", len(valid) + len(rejects), len(valid), len(rejects))
```

Notice that `run` takes functions for the outside world. In tests you pass fakes that return lists and collect writes; no disk required. This "inject the edges" style is how you keep ETL code testable, and you will lean on it heavily in the pipelines stage.

## Common mistakes

- Doing everything in one 80-line function: untestable and hard to change.
- Using `INSERT` on re-run and getting `UNIQUE constraint failed`, or worse, silent duplicates because there was no key.
- Committing per row (slow) or never committing (`conn.close()` without commit loses writes).
- Writing rejects without line numbers or reasons.
- Letting one bad row crash the whole run when the policy is to quarantine, or the opposite: continuing when 60% of rows are bad.

## What to take away

1. Extract, validate, transform and load are separate small functions; only the ends do I/O.
2. Rejected rows go to a file with line number and reason; write it even when empty.
3. Make loads idempotent: replace by key, in one transaction, with parameterised SQL.
4. Reconcile and log counts: `read = loaded + rejected`.
5. Inject the edges (readers and writers) so the middle is trivially testable.
