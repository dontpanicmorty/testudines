+++
id = "snowflake-patterns-offline.testing-warehouse-code"
title = "Testing warehouse code"
minutes = 30
+++

# Testing warehouse code

dbt gave you `unique`, `not_null` and unit tests for models. Python code that talks to Snowflake needs the same discipline, but you cannot spin up a warehouse for every `pytest` run. It would be slow, cost credits and need credentials. The answer is to design so the warehouse is a **replaceable part**.

> **dbt bridge.** A dbt unit test feeds a model fixed input rows and asserts the output rows. We do the same: fixed fake connection in, assert on statements and results out.

## Dependency injection: pass the connection in

```python
class FakeCursor:
    def __init__(self, rows): self.rows, self.closed = rows, False
    def execute(self, sql, params=None): self.sql, self.params = sql, params
    def fetchone(self): return self.rows[0] if self.rows else None
    def close(self): self.closed = True
    def __enter__(self): return self
    def __exit__(self, *a): self.close()

class FakeConn:
    def __init__(self, rows): self.rows, self.closed = rows, False
    def cursor(self): self.last = FakeCursor(self.rows); return self.last
    def close(self): self.closed = True

# Hard to test: creates its own connection inside.
# def revenue_for(day): conn = snowflake.connector.connect(...); ...

# Easy to test: the caller supplies a factory.
def revenue_for(connect, day: str) -> float:
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(amount) FROM orders WHERE order_date = %(d)s", {"d": day})
            row = cur.fetchone()
        return float(row[0] or 0)
    finally:
        conn.close()

conn = FakeConn([(125.5,)])
print(revenue_for(lambda: conn, "2026-11-02"), conn.closed)
print(conn.last.params)
```

Passing a **factory** (a zero-argument function) instead of a connection lets the function control when the connection opens and guarantees it closes. In production the factory is `lambda: snowflake.connector.connect(**params)`.

## Contract tests: what you assert on a fake

With a fake you can test three things the warehouse would never tell you directly:

1. **What SQL was sent** and with which parameters.
2. **What happens to results**: empty set, `NULL`, a duplicated row.
3. **Lifecycle**: connection closed, transaction committed or rolled back.

A **contract test** pins down the boundary: "when asked for revenue the function sends exactly one statement, with the date bound as a parameter, and closes the connection". If someone refactors and starts string-formatting the date, the test fails.

```python
def test_binds_date_and_closes():
    conn = FakeConn([(None,)])
    assert revenue_for(lambda: conn, "2026-01-01") == 0.0      # NULL sum becomes 0
    assert conn.last.params == {"d": "2026-01-01"}
    assert conn.closed

def revenue_for(connect, day):
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(amount) FROM orders WHERE order_date = %(d)s", {"d": day})
            row = cur.fetchone()
        return float(row[0] or 0)
    finally:
        conn.close()

class FakeCursor:
    def __init__(self, rows): self.rows = rows
    def execute(self, sql, params=None): self.params = params
    def fetchone(self): return self.rows[0]
    def __enter__(self): return self
    def __exit__(self, *a): pass

class FakeConn:
    def __init__(self, rows): self.rows, self.closed = rows, False
    def cursor(self): self.last = FakeCursor(self.rows); return self.last
    def close(self): self.closed = True

test_binds_date_and_closes()
print("contract holds")
```

## Comparing generated SQL

When code *builds* SQL (MERGE statements, `SELECT` lists), test the string. Normalise whitespace so formatting changes don't break tests, and compare the whole statement rather than `in` fragments:

```python
def normalise(sql: str) -> str:
    return " ".join(sql.split())

def select_columns(table: str, columns: list[str]) -> str:
    return f"SELECT {', '.join(columns)}\nFROM {table}"

assert normalise(select_columns("orders", ["id", "status"])) == "SELECT id, status FROM orders"
print("sql matches")
```

Beware **identifiers**: bind parameters cannot carry table or column names, so validate them (a strict regex such as `^[A-Za-z_][A-Za-z0-9_$]*$`) before they reach a string.

```python
import re

IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")

def ident(name: str) -> str:
    if not IDENT.match(name):
        raise ValueError(f"unsafe identifier: {name!r}")
    return name

print(ident("orders"))
try:
    ident("orders; DROP TABLE x")
except ValueError as e:
    print(e)
```

## DuckDB as a stand-in warehouse

Fakes verify *how you call* the database. They cannot tell you whether your SQL logic is right. For that, run the SQL on a real engine. DuckDB is in-process, instant, and understands most of the analytical SQL you write for Snowflake, including `QUALIFY`, window functions and `ROW_NUMBER`. Great for testing dedupe, latest-record and aggregation logic.

```python
import duckdb

con = duckdb.connect(":memory:")
con.execute("CREATE TABLE customers (id INTEGER, email TEXT, updated_at INTEGER)")
con.execute("""
    INSERT INTO customers VALUES
      (1, 'old@x.test', 1), (1, 'new@x.test', 2), (2, 'only@x.test', 5)
""")
latest = con.execute("""
    SELECT id, email FROM customers
    QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) = 1
    ORDER BY id
""").fetchall()
print(latest)
```

Know the seams: DuckDB uses `?`/`$name` placeholders (not `%(name)s`), has no `COPY INTO @stage`, and differs on semi-structured types and some functions. Keep SQL that you want to test portable, and put engine-specific parts behind a small adapter:

```python
import re
import duckdb

class DuckAdapter:
    """Lets code written with %(name)s placeholders run on DuckDB."""
    def __init__(self):
        self._con = duckdb.connect(":memory:")

    def execute(self, sql, params=None):
        sql = re.sub(r"%\((\w+)\)s", r"$\1", sql)
        self._con.execute(sql, params or {})
        return self._con

db = DuckAdapter()
db.execute("CREATE TABLE t (region TEXT, amount INTEGER)")
db.execute("INSERT INTO t VALUES ('EU', 10), ('US', 20), ('EU', 5)")
print(db.execute("SELECT SUM(amount) FROM t WHERE region = %(r)s", {"r": "EU"}).fetchone())
```

Test pyramid for this work: many fast fake-based contract tests; some DuckDB logic tests; and, outside this course, a few integration runs against a real dev warehouse.

## Common mistakes

- Creating the connection at import time or inside the function, which forces a real warehouse in every test.
- Assertions like `assert "WHERE" in sql`: too loose to catch real regressions.
- A fake that returns whatever you hope for, with no empty-result or `NULL` cases tested.
- Treating DuckDB passing as proof of Snowflake behaviour for engine-specific functions.
- Formatting values into SQL so the contract test cannot check parameters.
- Forgetting to assert cleanup: the connection leaks and no test notices.

## What to take away

1. Inject the connection (or a factory) so tests can replace it.
2. Contract-test statements, parameters, edge-case results and cleanup on a fake.
3. Normalise whitespace and compare generated SQL whole.
4. Validate identifiers; bind values.
5. Use DuckDB to test SQL logic, and know where it differs from Snowflake.
