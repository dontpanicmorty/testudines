+++
id = "snowflake-patterns-offline.connector-anatomy"
title = "Connector anatomy and fakes"
minutes = 30
+++

# Connector anatomy and fakes

You know what Snowflake does with a query. This module is about the other half: the Python object model around it. Here there is **no real connection**. We study the shape of the official connector, then write a fake with the same shape so everything is testable offline.

> **Snowflake bridge.** A worksheet hides the plumbing: sign in, pick role and warehouse, run, read the grid. Python makes each step an explicit object: **connection** (session), **cursor** (one statement's results), **execute**, **fetch**, **close**.

## The lifecycle

This is what real code looks like. It is marked `no-run` because the learner environment has no Snowflake:

```python
# no-run
import snowflake.connector

conn = snowflake.connector.connect(
    account="myorg-myaccount", user="SVC_LOADER", authenticator="snowflake_jwt",
    private_key_file="/secrets/key.p8", role="LOADER", warehouse="LOAD_WH",
    database="RAW", schema="PUBLIC",
)
cur = conn.cursor()
try:
    cur.execute("SELECT id, name FROM customers WHERE region = %(region)s", {"region": "EU"})
    for row in cur.fetchall():
        print(row)          # tuples: (1, 'Ada')
finally:
    cur.close()
    conn.close()
```

Five ideas:

1. `connect(...)` opens a **session** with role, warehouse, database and schema set. It is expensive: create it once per job, not per query.
2. `conn.cursor()` is cheap: one per statement or logical step.
3. `cur.execute(sql, params)` sends SQL; `params` are bound for you.
4. `fetchone()` returns one tuple (or `None`), `fetchmany(n)` a list of at most n, `fetchall()` everything. `cur.description` lists the columns; `cur.rowcount` is the affected/returned count.
5. Close the cursor and connection even when something fails.

## Context managers do the closing

`with` guarantees cleanup, the way `try/finally` does but in one line. Both cursors and connections support it.

```python
class Resource:
    def __init__(self, name): self.name, self.closed = name, False
    def __enter__(self): print("open", self.name); return self
    def __exit__(self, exc_type, exc, tb):
        self.closed = True
        print("close", self.name, "error?", exc_type is not None)
        return False          # do not swallow the exception

try:
    with Resource("cursor") as r:
        raise RuntimeError("query failed")
except RuntimeError as e:
    print("caught:", e, r.closed)
```

So real code is simply:

```python
# no-run
with snowflake.connector.connect(**params) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        print(cur.fetchone())
```

## A fake with the same shape

If your job logic only talks to "something with `.cursor()`, `.execute()`, `.fetchall()`", a hand-written fake can stand in. This one runs SQL on an in-memory SQLite database, enough to test logic. It also records every statement, which is gold for asserting behaviour.

```python
import re
import sqlite3

class FakeCursor:
    def __init__(self, conn):
        self._conn, self._cur, self.closed = conn, conn._db.cursor(), False

    def execute(self, sql, params=None):
        sql, params = self._conn._translate(sql, params)
        self._conn.executed.append((sql, params))
        self._cur.execute(sql, params)
        return self

    @property
    def description(self):
        return self._cur.description

    def fetchone(self): return self._cur.fetchone()
    def fetchall(self): return self._cur.fetchall()
    def close(self): self.closed = True
    def __enter__(self): return self
    def __exit__(self, *exc): self.close()

class FakeConnection:
    def __init__(self):
        self._db = sqlite3.connect(":memory:")
        self.executed, self.closed = [], False

    def _translate(self, sql, params):
        sql = re.sub(r"%\((\w+)\)s", r":\1", sql)      # pyformat -> named
        return sql, params or {}

    def cursor(self): return FakeCursor(self)
    def close(self): self.closed = True
    def __enter__(self): return self
    def __exit__(self, *exc): self.close()

conn = FakeConnection()
with conn.cursor() as cur:
    cur.execute("CREATE TABLE customers (id INTEGER, name TEXT, region TEXT)")
    cur.execute("INSERT INTO customers VALUES (1, 'Ada', 'EU')")
    cur.execute("INSERT INTO customers VALUES (2, 'Linus', 'US')")
    cur.execute("SELECT id, name FROM customers WHERE region = %(region)s", {"region": "EU"})
    print(cur.fetchall())
print(len(conn.executed), "statements recorded")
```

## Parameter binding styles

Never format values into SQL with f-strings. Besides injection, quoting and type edge cases are the connector's job.

| Style | Looks like | Notes |
|---|---|---|
| pyformat (default) | `%(name)s` with a dict | readable, recommended |
| format | `%s` with a tuple/list | positional |
| qmark | `?` with a tuple | enabled via the connector's `paramstyle` setting |

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE t (id INTEGER, note TEXT)")
db.execute("INSERT INTO t VALUES (?, ?)", (1, "it's fine"))     # the quote is handled safely
print(db.execute("SELECT * FROM t").fetchall())

evil = "x'; DROP TABLE t; --"
print(db.execute("SELECT count(*) FROM t WHERE note = ?", (evil,)).fetchone())
```

Bind **values**. Identifiers (table, column names) cannot be bound; validate those against an allow-list or a pattern instead.

## Rows as dicts

Default fetches give tuples; you then index by position, which breaks when someone adds a column. The connector offers `DictCursor`, which returns dicts keyed by column name (Snowflake upper-cases unquoted names, so keys are `ID`, `NAME`). You can build the same thing from `cursor.description`:

```python
import sqlite3

def rows_as_dicts(cur) -> list[dict]:
    if cur.description is None:          # statement returned no result set
        return []
    names = [d[0].lower() for d in cur.description]
    return [dict(zip(names, row)) for row in cur.fetchall()]

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE o (id INTEGER, status TEXT)")
db.executemany("INSERT INTO o VALUES (?, ?)", [(1, "shipped"), (2, "open")])
print(rows_as_dicts(db.execute("SELECT * FROM o ORDER BY id")))
```

Build a **new** dict per row. Reusing one dict and appending it repeatedly gives you N references to the same last row.

## Dependency injection in one line

```python
def count_rows(conn, table_name: str) -> int:
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")   # identifier validated elsewhere
        return cur.fetchone()[0]
```

`count_rows` never creates a connection. Production passes a real one; tests pass a fake.

## Common mistakes

- Forgetting to close: warehouses stay busy and sessions pile up. Use `with`.
- Opening a new connection for every query. Authentication round trips dominate the runtime.
- `cur.fetchone()[0]` when there are no rows: `TypeError: 'NoneType' object is not subscriptable`. Check for `None`.
- f-string SQL with user values. Bind them.
- Assuming column order or case. Names come back upper-case from Snowflake; use dict rows and normalise.
- Appending the same dict repeatedly in a loop, so every result row is identical.

## What to take away

1. Connect once, make a cursor per statement, execute, fetch, close.
2. `with` blocks guarantee cleanup, including on exceptions.
3. Bind values with parameters; validate identifiers separately.
4. Prefer dict rows over positional tuples.
5. Write code against "a connection", then test it with a hand-written fake that records statements.
