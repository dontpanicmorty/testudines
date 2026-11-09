+++
id = "sql-from-python.duckdb-for-analytics"
title = "DuckDB: analytic SQL inside Python"
minutes = 30
+++

# DuckDB: analytic SQL inside Python

SQLite is built for application data: lots of small reads and writes. Your day job is analytics: scans, joins, window functions over millions of rows. **DuckDB** is an in-process analytic engine with a Snowflake-flavoured SQL dialect. Everything you know about CTEs, `QUALIFY`, window frames and `GROUP BY` transfers directly, and it reads CSV and Parquet files without a load step.

> **SQL bridge.** DuckDB is like a tiny local Snowflake: columnar, vectorised, with `COPY`, `read_csv_auto` (think external stage + `INFER_SCHEMA`), and `QUALIFY`.

## An in-memory database

```python
import duckdb

con = duckdb.connect()            # in-memory
print(con.execute("SELECT 40 + 2 AS answer").fetchall())
```

`execute` returns the connection itself, so you chain a fetch: `fetchall()` gives a list of tuples, `fetchone()` one tuple, `fetchdf()` a pandas DataFrame, `pl()` a polars DataFrame.

## Query files directly

The bundled datasets are CSVs. `read_csv_auto` infers column names and types:

```python
import os, duckdb

data = os.environ["DOJO_DATA"]
con = duckdb.connect()
rows = con.execute(
    "SELECT region, COUNT(*) AS n FROM read_csv_auto(?) GROUP BY region ORDER BY n DESC, region",
    [f"{data}/customers.csv"],
).fetchall()
print(rows)
```

Look: the file path is passed as a **parameter**, same rule as the last lesson. Placeholders work for values, including the argument of `read_csv_auto`.

To reuse a file, make a view so later queries read like a normal warehouse:

```python
import os, duckdb

data = os.environ["DOJO_DATA"]
con = duckdb.connect()
for name in ["customers", "orders", "order_items"]:
    con.execute(f"CREATE VIEW {name} AS SELECT * FROM read_csv_auto('{data}/{name}.csv')")

print(con.execute("DESCRIBE orders").fetchall())
```

`CREATE VIEW` cannot be prepared, so the path and the name are formatted into the text. That is acceptable here because both come from our own code (a hard-coded list and a trusted directory), never from user input.

## CTEs and window functions

Your SQL knowledge works as-is. Revenue per customer, ranked, using a CTE and a window:

```python
import os, duckdb

data = os.environ["DOJO_DATA"]
con = duckdb.connect()
for name in ["orders", "order_items"]:
    con.execute(f"CREATE VIEW {name} AS SELECT * FROM read_csv_auto('{data}/{name}.csv')")

sql = """
WITH revenue AS (
    SELECT o.customer_id, SUM(i.quantity * i.unit_price) AS revenue
    FROM orders o JOIN order_items i USING (order_id)
    WHERE o.status <> 'cancelled'
    GROUP BY o.customer_id
)
SELECT customer_id, ROUND(revenue, 2) AS revenue,
       RANK() OVER (ORDER BY revenue DESC) AS rnk
FROM revenue
QUALIFY rnk <= 3
ORDER BY rnk, customer_id
"""
for row in con.execute(sql).fetchall():
    print(row)
```

`QUALIFY` filters on a window function, exactly as in Snowflake. Running totals are a window with a frame:

```python
import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE sales (day DATE, amount DOUBLE)")
con.executemany("INSERT INTO sales VALUES (?, ?)",
                [("2025-01-01", 10), ("2025-01-02", 5), ("2025-01-03", 20)])
print(con.execute("""
    SELECT day, amount,
           SUM(amount) OVER (ORDER BY day) AS running
    FROM sales ORDER BY day
""").fetchall())
```

## Python values in, Python values out

Rows come back as tuples with proper Python types (`datetime.date`, `Decimal`, `float`). If you want dicts, ask for column names:

```python
import duckdb

con = duckdb.connect()
cur = con.execute("SELECT 1 AS id, 'Ada' AS name UNION ALL SELECT 2, 'Linus' ORDER BY id")
cols = [d[0] for d in cur.description]
print([dict(zip(cols, row)) for row in cur.fetchall()])
```

DuckDB can also query a Python DataFrame in scope by its variable name (a "replacement scan"), which is handy for mixing tools:

```python
import duckdb, pandas as pd

df = pd.DataFrame({"plan": ["pro", "free", "pro"], "mrr": [50, 0, 70]})
print(duckdb.sql("SELECT plan, SUM(mrr) AS mrr FROM df GROUP BY plan ORDER BY plan").fetchall())
```

## Parquet round trip

Parquet is the columnar file format your lake and warehouse stages speak. It preserves types, unlike CSV.

```python
import duckdb, tempfile, pathlib

out = pathlib.Path(tempfile.mkdtemp()) / "nums.parquet"
con = duckdb.connect()
con.execute("CREATE TABLE t AS SELECT range AS n, range * 1.5 AS x FROM range(5)")
con.execute(f"COPY t TO '{out}' (FORMAT PARQUET)")       # path built by us, not user input
print(con.execute("SELECT COUNT(*), SUM(x) FROM read_parquet(?)", [str(out)]).fetchall())
print(out.stat().st_size > 0)
```

## Common mistakes

- Treating DuckDB like a server: it runs in your process. An in-memory database disappears when the connection is closed; pass a filename to `duckdb.connect("file.duckdb")` to keep it.
- Opening one file database from two processes for writing: `duckdb.IOException: Could not set lock on file`.
- Using a Python variable in `FROM` that is not in scope: `Catalog Error: Table with name df does not exist!`.
- `COPY ... TO` and `CREATE VIEW` do not accept `?` for the *path*, so you format it into the text. Only do that with paths you built yourself.
- Forgetting `ORDER BY`: result order is not guaranteed without it. Tests that compare lists need a total order.

## What to take away

1. DuckDB runs your analytic SQL, CTEs, windows and `QUALIFY`, inside Python with no server.
2. `read_csv_auto` and `read_parquet` query files directly; views make them tables.
3. `execute(...).fetchall()` gives tuples, `.description` gives column names, `.fetchdf()` / `.pl()` hand off to pandas and polars.
4. Pass values (even file paths in `read_*`) as parameters.
5. Parquet keeps types and is the right interchange format; always add `ORDER BY` when you need deterministic results.
