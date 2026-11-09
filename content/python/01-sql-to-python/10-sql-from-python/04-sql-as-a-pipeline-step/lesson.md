+++
id = "sql-from-python.sql-as-a-pipeline-step"
title = "SQL as a pipeline step"
minutes = 30
+++

# SQL as a pipeline step

A dbt model is a `SELECT` plus a promise: run it again and you get the same table. That promise, **idempotency**, is what makes pipelines safe to retry. In this lesson you rebuild the three ideas that make dbt work, in plain Python: idempotent writes, SQL kept in template files, and `ref()` resolving dependencies.

> **SQL bridge.** `CREATE OR REPLACE TABLE x AS SELECT ...` is a dbt "table" materialization. `MERGE` is an incremental model with a `unique_key`. `{{ ref('x') }}` is a dependency edge plus a name substitution.

## Idempotent builds

Running a load twice must not duplicate rows. The simplest idempotent step rebuilds the whole target:

```python
import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE raw_orders AS SELECT * FROM (VALUES (1, 'a', 10), (2, 'b', 20)) t(id, cust, amt)")

def build_revenue(con):
    con.execute("""
        CREATE OR REPLACE TABLE revenue AS
        SELECT cust, SUM(amt) AS total FROM raw_orders GROUP BY cust
    """)

build_revenue(con)
build_revenue(con)          # same result the second time
print(con.execute("SELECT * FROM revenue ORDER BY cust").fetchall())
```

> **Predict first.** If the step were `INSERT INTO revenue SELECT ...` instead, what would two runs produce?

Duplicates: each run appends. `INSERT` is not idempotent; `CREATE OR REPLACE` is.

## Upserts for incremental loads

Rebuilding is wasteful for large tables. An **upsert** inserts new keys and updates existing ones. SQLite and DuckDB both support `INSERT ... ON CONFLICT (key) DO UPDATE`:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, email TEXT, updated_at TEXT)")

UPSERT = """
INSERT INTO customers (id, email, updated_at) VALUES (:id, :email, :updated_at)
ON CONFLICT (id) DO UPDATE SET
    email = excluded.email,
    updated_at = excluded.updated_at
WHERE excluded.updated_at > customers.updated_at
"""
batch = [{"id": 1, "email": "a@x.com", "updated_at": "2025-01-02"}]
late  = [{"id": 1, "email": "OLD@x.com", "updated_at": "2025-01-01"}]
with conn:
    conn.executemany(UPSERT, batch)
    conn.executemany(UPSERT, late)       # a late-arriving, older record
    conn.executemany(UPSERT, batch)      # replay
print(conn.execute("SELECT * FROM customers").fetchall())
```

`excluded` is the row you tried to insert. The `WHERE` clause on the update is the guard against **late-arriving data**: an older version must never overwrite a newer one. Compare to `INSERT OR REPLACE`, which deletes and re-inserts blindly and has no such guard.

## SQL lives in files

Long SQL does not belong inside Python strings scattered through code. Keep each model as a `.sql` file and let Python read and run it:

```python
import duckdb, tempfile, pathlib

sql_dir = pathlib.Path(tempfile.mkdtemp())
(sql_dir / "totals.sql").write_text("SELECT cust, SUM(amt) AS total FROM raw GROUP BY cust")

con = duckdb.connect()
con.execute("CREATE TABLE raw AS SELECT * FROM (VALUES ('a', 1), ('a', 2), ('b', 5)) t(cust, amt)")
query = (sql_dir / "totals.sql").read_text()
print(con.execute(f"SELECT * FROM ({query}) ORDER BY cust").fetchall())
```

## A tiny `ref()`

dbt's `{{ ref('model') }}` does two jobs: substitute the table name, and tell dbt the order to build things. You can render it with one regular expression. Read it slowly, it is the entire trick:

```python
import re

REF = re.compile(r"\{\{\s*ref\(\s*'([^']+)'\s*\)\s*\}\}")

def render(template: str, relations: dict[str, str]) -> str:
    def replace(match: re.Match) -> str:
        name = match.group(1)
        if name not in relations:
            raise KeyError(f"unknown model {name!r}")
        return relations[name]
    return REF.sub(replace, template)

sql = "SELECT * FROM {{ ref('stg_orders') }} JOIN {{ ref( 'stg_customers' ) }} USING (cust_id)"
print(render(sql, {"stg_orders": "analytics.stg_orders", "stg_customers": "analytics.stg_customers"}))
```

`re.sub` accepts a function: it is called for each match and its return value replaces the match. The same regex, run with `findall`, gives you the dependencies:

```python
import re

REF = re.compile(r"\{\{\s*ref\(\s*'([^']+)'\s*\)\s*\}\}")
print(REF.findall("SELECT * FROM {{ ref('a') }} JOIN {{ ref('b') }}"))
```

## Ordering with a graph

Once every model lists its parents, `graphlib` from the standard library sorts them so parents build first, and detects cycles:

```python
from graphlib import TopologicalSorter

deps = {"revenue": {"stg_orders", "stg_customers"}, "stg_orders": set(), "stg_customers": set()}
print(list(TopologicalSorter(deps).static_order()))
```

Render, sort, then run each as `CREATE OR REPLACE TABLE name AS <sql>`. That is a mini dbt, and the exercises build it.

## Common mistakes

- Using plain `INSERT` in a step you intend to retry. You get silent duplicates.
- `INSERT OR REPLACE` in SQLite: replaces the whole row, even with older data. Prefer `ON CONFLICT ... DO UPDATE ... WHERE`.
- `sqlite3.OperationalError: ON CONFLICT clause does not match any PRIMARY KEY or UNIQUE constraint`: the conflict target needs a unique index.
- Rendering with `str.replace` for each model: fails on whitespace variants like `{{ ref( 'x' ) }}`. Use a regex.
- Substituting *values* with a template renderer. Templates are for **identifiers and structure you control**; values still go through parameters.

## What to take away

1. A pipeline step you might retry must be idempotent: `CREATE OR REPLACE` or an upsert, never a bare `INSERT`.
2. Upsert with `ON CONFLICT (key) DO UPDATE`, guarded by a timestamp comparison for late data.
3. Keep SQL in `.sql` files and run it from Python.
4. `ref()` is a regex substitution plus dependency discovery; `graphlib.TopologicalSorter` orders the build.
5. Templates for names, parameters for values.
