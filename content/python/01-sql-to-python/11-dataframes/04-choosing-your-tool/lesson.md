+++
id = "dataframes.choosing-your-tool"
title = "Choosing your tool"
minutes = 30
+++

# Choosing your tool

You now have four ways to do the same table work: plain Python, DuckDB, pandas and polars. None is "best". A production engineer picks by **data size, team skills and the surrounding code**. This lesson solves one task four ways so you can see the trade-offs, then gives you a decision guide.

> **SQL bridge.** It is the same decision you made choosing between a view, a dbt model, a Snowflake task and a Python UDF: the right tool is the one that fits the data volume and the people who will maintain it.

## The task

For each customer: total revenue from non-cancelled orders, top 3 customers, ties broken by lower `customer_id`. Our inputs are lists of dicts, as an API or JSON file would give you.

```python
orders = [
    {"order_id": 1, "customer_id": 10, "status": "shipped"},
    {"order_id": 2, "customer_id": 20, "status": "cancelled"},
    {"order_id": 3, "customer_id": 20, "status": "completed"},
    {"order_id": 4, "customer_id": 30, "status": "completed"},
]
items = [
    {"order_id": 1, "quantity": 2, "unit_price": 10.0},
    {"order_id": 2, "quantity": 9, "unit_price": 99.0},
    {"order_id": 3, "quantity": 1, "unit_price": 25.0},
    {"order_id": 3, "quantity": 1, "unit_price": 5.0},
    {"order_id": 4, "quantity": 3, "unit_price": 10.0},
]
```

## Plain Python

```python
from collections import defaultdict

def top_python(orders, items, n=3):
    owner = {o["order_id"]: o["customer_id"] for o in orders if o["status"] != "cancelled"}
    totals = defaultdict(float)
    for it in items:
        cust = owner.get(it["order_id"])
        if cust is not None:
            totals[cust] += it["quantity"] * it["unit_price"]
    ranked = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    return [(c, round(t, 2)) for c, t in ranked[:n]]

orders = [{"order_id": 1, "customer_id": 10, "status": "shipped"}, {"order_id": 2, "customer_id": 20, "status": "cancelled"},
          {"order_id": 3, "customer_id": 20, "status": "completed"}, {"order_id": 4, "customer_id": 30, "status": "completed"}]
items = [{"order_id": 1, "quantity": 2, "unit_price": 10.0}, {"order_id": 2, "quantity": 9, "unit_price": 99.0},
         {"order_id": 3, "quantity": 1, "unit_price": 25.0}, {"order_id": 3, "quantity": 1, "unit_price": 5.0},
         {"order_id": 4, "quantity": 3, "unit_price": 10.0}]
print(top_python(orders, items))
```

Fast to write, zero dependencies, easy to test. It gets slow and memory-hungry past a few million rows, and every new question means more loops.

## DuckDB

```python
import duckdb

def top_duckdb(orders, items, n=3):
    con = duckdb.connect()
    con.execute("CREATE TABLE o (order_id BIGINT, customer_id BIGINT, status VARCHAR)")
    con.execute("CREATE TABLE i (order_id BIGINT, quantity BIGINT, unit_price DOUBLE)")
    con.executemany("INSERT INTO o VALUES (?, ?, ?)", [[r["order_id"], r["customer_id"], r["status"]] for r in orders])
    con.executemany("INSERT INTO i VALUES (?, ?, ?)", [[r["order_id"], r["quantity"], r["unit_price"]] for r in items])
    rows = con.execute("""
        SELECT o.customer_id, ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue
        FROM o JOIN i USING (order_id) WHERE o.status <> 'cancelled'
        GROUP BY 1 ORDER BY revenue DESC, 1 LIMIT ?""", [n]).fetchall()
    return [(int(c), float(r)) for c, r in rows]

orders = [{"order_id": 1, "customer_id": 10, "status": "shipped"}, {"order_id": 2, "customer_id": 20, "status": "cancelled"},
          {"order_id": 3, "customer_id": 20, "status": "completed"}, {"order_id": 4, "customer_id": 30, "status": "completed"}]
items = [{"order_id": 1, "quantity": 2, "unit_price": 10.0}, {"order_id": 2, "quantity": 9, "unit_price": 99.0},
         {"order_id": 3, "quantity": 1, "unit_price": 25.0}, {"order_id": 3, "quantity": 1, "unit_price": 5.0},
         {"order_id": 4, "quantity": 3, "unit_price": 10.0}]
print(top_duckdb(orders, items))
```

This is the one you can write without thinking. Larger-than-memory files, joins and window functions are its home ground.

## pandas

```python
import pandas as pd

def top_pandas(orders, items, n=3):
    o = pd.DataFrame(orders).query("status != 'cancelled'")
    df = o.merge(pd.DataFrame(items), on="order_id")
    df = df.assign(revenue=df["quantity"] * df["unit_price"])
    out = df.groupby("customer_id", as_index=False)["revenue"].sum()
    out = out.sort_values(["revenue", "customer_id"], ascending=[False, True]).head(n)
    return [(int(c), round(float(r), 2)) for c, r in zip(out["customer_id"], out["revenue"])]

orders = [{"order_id": 1, "customer_id": 10, "status": "shipped"}, {"order_id": 2, "customer_id": 20, "status": "cancelled"},
          {"order_id": 3, "customer_id": 20, "status": "completed"}, {"order_id": 4, "customer_id": 30, "status": "completed"}]
items = [{"order_id": 1, "quantity": 2, "unit_price": 10.0}, {"order_id": 2, "quantity": 9, "unit_price": 99.0},
         {"order_id": 3, "quantity": 1, "unit_price": 25.0}, {"order_id": 3, "quantity": 1, "unit_price": 5.0},
         {"order_id": 4, "quantity": 3, "unit_price": 10.0}]
print(top_pandas(orders, items))
```

The default in the wider ecosystem: plotting, machine learning, and countless libraries accept a pandas frame. Memory use is high (often several times the file size).

## polars

```python
import polars as pl

def top_polars(orders, items, n=3):
    o = pl.DataFrame(orders).filter(pl.col("status") != "cancelled")
    out = (
        o.join(pl.DataFrame(items), on="order_id")
        .group_by("customer_id")
        .agg((pl.col("quantity") * pl.col("unit_price")).sum().round(2).alias("revenue"))
        .sort(["revenue", "customer_id"], descending=[True, False])
        .head(n)
    )
    return [(int(c), float(r)) for c, r in zip(out["customer_id"], out["revenue"])]

orders = [{"order_id": 1, "customer_id": 10, "status": "shipped"}, {"order_id": 2, "customer_id": 20, "status": "cancelled"},
          {"order_id": 3, "customer_id": 20, "status": "completed"}, {"order_id": 4, "customer_id": 30, "status": "completed"}]
items = [{"order_id": 1, "quantity": 2, "unit_price": 10.0}, {"order_id": 2, "quantity": 9, "unit_price": 99.0},
         {"order_id": 3, "quantity": 1, "unit_price": 25.0}, {"order_id": 3, "quantity": 1, "unit_price": 5.0},
         {"order_id": 4, "quantity": 3, "unit_price": 10.0}]
print(top_polars(orders, items))
```

Fast, parallel, strict types, great expression API. Smaller ecosystem than pandas, but conversion is one call (`.to_pandas()`).

## A decision guide

| Situation | Reach for |
|---|---|
| A few thousand rows, nested API data, no heavy maths | plain Python |
| Files or tables from tens of MB to many GB; SQL-fluent team | DuckDB |
| Feeding a plotting or ML library; notebooks; legacy code already pandas | pandas |
| A production pipeline with complex column logic; speed and strictness matter | polars |
| Data already lives in the warehouse | Do it in SQL there; pull only the result into Python |

Some rules that outlast any benchmark:

1. **Move the compute to the data.** Never pull a billion warehouse rows into Python to aggregate them.
2. **Match the team.** A SQL-first team maintains DuckDB queries happily; a pandas-first team will not enjoy polars lazy plans, and vice versa.
3. **Do not mix tools inside one function** without a reason. Pick one for the transform and convert at the edges: `duckdb ... .pl()`, `polars ... .to_pandas()`.
4. **Test equivalence.** If you ever migrate a transform between tools, run both on the same fixture and assert identical output. That is what the exercises ask you to do.

## Making results agree

Different tools disagree in small ways that bite: float rounding, how ties and `NULL`s sort, integer versus float dtype, group order. To compare results, convert to plain Python values (`int`, `float`), round money, and sort with an explicit total order.

## Common mistakes

- Comparing a pandas `numpy.int64` to an `int` in an `assert` and getting a type surprise. Convert with `int(...)`.
- Comparing floats exactly after different summation orders. Round, or use `pytest.approx`.
- Forgetting a tie-breaker in the sort so two tools legitimately return different but "correct" orders.
- Reaching for pandas by habit when a single SQL statement in DuckDB would be shorter.

## What to take away

1. The same task is a few lines in any of the four tools; choose by size, ecosystem and team.
2. DuckDB for SQL-shaped analytics on files, pandas for the ecosystem, polars for fast typed pipelines, plain Python for small and nested data.
3. Push work to the warehouse before pulling data into Python.
4. Convert at the boundaries and keep one tool per transform.
5. Always give comparisons a total sort order and normalise types and rounding.
