+++
id = "sql-from-python.sqlite-basics"
title = "sqlite3: connections, cursors and transactions"
minutes = 25
+++

# sqlite3: connections, cursors and transactions

You have written SQL for years. Python's job here is only to *carry* your SQL to a database and bring the rows back. `sqlite3` ships with Python, needs no server, and can live entirely in memory, which makes it the perfect place to learn the pattern every database driver follows (Snowflake's connector, Postgres drivers and DuckDB all look much the same).

> **SQL bridge.** A Snowflake worksheet session is a *connection*. Each statement you run is an `execute`. `COMMIT` and `ROLLBACK` are methods on the connection.

## Connect, execute, fetch

```python
import sqlite3

conn = sqlite3.connect(":memory:")   # a throwaway database in RAM
conn.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, plan TEXT)")
conn.execute("INSERT INTO customers VALUES (1, 'Ada', 'pro')")
conn.execute("INSERT INTO customers VALUES (2, 'Linus', 'free')")

cur = conn.execute("SELECT id, name FROM customers ORDER BY id")
print(cur.fetchall())
conn.close()
```

`conn.execute(...)` returns a **cursor**: a handle on the result set. You pull rows from it with `fetchone()`, `fetchmany(n)` or `fetchall()`. A cursor is also iterable, which streams rows instead of loading everything:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (n INTEGER)")
conn.executemany("INSERT INTO t VALUES (?)", [(1,), (2,), (3,)])
for (n,) in conn.execute("SELECT n FROM t"):
    print(n)
```

> **Predict first.** After `cur.fetchall()` returns, what does a second `cur.fetchall()` give?

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (n INTEGER)")
conn.execute("INSERT INTO t VALUES (1)")
cur = conn.execute("SELECT n FROM t")
print(cur.fetchall())
print(cur.fetchall())
```

An empty list. A cursor is consumed as you read it. If you need the rows twice, keep the list.

## Rows: tuples are fragile

By default each row is a tuple, so you must remember that `row[2]` means `plan`. Set a **row factory** and columns become addressable by name:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.execute("CREATE TABLE customers (id INTEGER, name TEXT, plan TEXT)")
conn.execute("INSERT INTO customers VALUES (1, 'Ada', 'pro')")

row = conn.execute("SELECT * FROM customers").fetchone()
print(row["name"], row["plan"])
print(dict(row))
print(row.keys())
```

`dict(row)` is the bridge to everything else in Python: JSON, pandas, pydantic models.

## Transactions

Python's `sqlite3` opens a transaction automatically before an `INSERT`, `UPDATE` or `DELETE`. Nothing is permanent until you call `conn.commit()`. A second connection to the same file will not see uncommitted rows.

The idiomatic way is to use the connection as a **context manager**: it commits if the block succeeds and rolls back if it raises.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE acct (id INTEGER PRIMARY KEY, balance INTEGER)")
conn.execute("INSERT INTO acct VALUES (1, 100), (2, 50)")
conn.commit()

try:
    with conn:                     # one transaction
        conn.execute("UPDATE acct SET balance = balance - 80 WHERE id = 1")
        raise RuntimeError("crash between the two updates")
        conn.execute("UPDATE acct SET balance = balance + 80 WHERE id = 2")
except RuntimeError as exc:
    print("failed:", exc)

print(conn.execute("SELECT * FROM acct ORDER BY id").fetchall())
```

The debit was rolled back, so `[(1, 100), (2, 50)]`. This is exactly what `BEGIN ... COMMIT` gives you in a warehouse, except Python decides when to roll back from whether an exception escaped.

Important: `with conn:` does **not** close the connection. To also close it, wrap with `contextlib.closing`:

```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as conn:
    with conn:
        conn.execute("CREATE TABLE t (n INTEGER)")
        conn.execute("INSERT INTO t VALUES (7)")
    print(conn.execute("SELECT n FROM t").fetchone())
```

## Files and idempotent setup

A path instead of `:memory:` gives you a file that persists. Use `CREATE TABLE IF NOT EXISTS` so setup code can run every time without failing; in pipelines, anything that is safe to run twice is worth gold.

```python
import sqlite3, tempfile, pathlib

path = pathlib.Path(tempfile.mkdtemp()) / "demo.db"
for _ in range(2):                       # second pass must not fail
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY, note TEXT)")
    conn.execute("INSERT INTO runs (note) VALUES ('hello')")
    conn.commit()
    conn.close()
print(sqlite3.connect(path).execute("SELECT COUNT(*) FROM runs").fetchone())
```

One more habit: SQLite does not enforce foreign keys unless you ask each connection with `PRAGMA foreign_keys = ON`.

## Common mistakes

- **Forgetting to commit.** Everything looks fine in your session, then the data is missing from the file. Use `with conn:`.
- **Reading a cursor twice.** The second `fetchall()` returns `[]`, not an error, which makes it a silent bug.
- **Assuming `with conn:` closes it.** It only manages the transaction.
- **Column by position.** `row[3]` breaks the day someone reorders the `SELECT`. Use `sqlite3.Row`.
- **Writing from two connections at once** can raise `sqlite3.OperationalError: database is locked`. Keep transactions short.

## What to take away

1. A connection is a session; `execute` returns a cursor, which is consumed as you read.
2. Set `row_factory = sqlite3.Row` and convert with `dict(row)`.
3. Nothing is durable until commit. Prefer `with conn:` so errors roll back.
4. `closing(...)` closes; `with conn` only commits or rolls back.
5. Make setup idempotent with `IF NOT EXISTS` and turn on foreign keys per connection.
