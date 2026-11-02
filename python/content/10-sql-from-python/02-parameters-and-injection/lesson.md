+++
id = "sql-from-python.parameters-and-injection"
title = "Parameters, injection and bulk loads"
minutes = 25
+++

# Parameters, injection and bulk loads

In dbt you build SQL with Jinja, and in Snowflake scripting you might concatenate strings to make a statement. In Python you will be tempted to do the same with f-strings. **Do not.** Mixing data into SQL text is how SQL injection happens, and it also breaks on innocent data like a customer named `O'Brien`.

> **SQL bridge.** A parameter is like a bind variable (`:name` or `?`) in a prepared statement. The *statement* and the *values* travel separately, so values can never be mistaken for SQL.

## The bug

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (id INTEGER, name TEXT, plan TEXT)")
conn.executemany("INSERT INTO customers VALUES (?, ?, ?)",
                 [(1, "Ada", "pro"), (2, "Linus", "free"), (3, "O'Brien", "pro")])

name = "O'Brien"
try:
    conn.execute(f"SELECT * FROM customers WHERE name = '{name}'").fetchall()
except sqlite3.OperationalError as exc:
    print("broke on honest data:", exc)
```

The apostrophe ended the string literal early. Now imagine a value that is not honest:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (id INTEGER, name TEXT, plan TEXT)")
conn.execute("INSERT INTO customers VALUES (1, 'Ada', 'pro')")

evil = "x' OR '1'='1"
sql = f"SELECT * FROM customers WHERE name = '{evil}'"
print(sql)
print(conn.execute(sql).fetchall())   # returns every row
```

## The fix: placeholders

Write `?` where a value goes and pass the values as a second argument, a tuple or list.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (id INTEGER, name TEXT, plan TEXT)")
conn.executemany("INSERT INTO customers VALUES (?, ?, ?)",
                 [(1, "Ada", "pro"), (2, "Linus", "free"), (3, "O'Brien", "pro")])

print(conn.execute("SELECT * FROM customers WHERE name = ?", ("O'Brien",)).fetchall())
print(conn.execute("SELECT * FROM customers WHERE name = ?", ("x' OR '1'='1",)).fetchall())
```

Note the one-element tuple `("O'Brien",)`: the trailing comma matters. `("O'Brien")` is just a string, and sqlite3 would treat each character as a separate parameter.

Named placeholders read better with many values and take a dict:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (id INTEGER, name TEXT, plan TEXT)")
conn.execute("INSERT INTO customers VALUES (:id, :name, :plan)",
             {"id": 1, "name": "Ada", "plan": "pro"})
print(conn.execute("SELECT * FROM customers WHERE plan = :p", {"p": "pro"}).fetchall())
```

## Bulk inserts with `executemany`

One `execute` per row is slow and chatty. `executemany` sends the same statement with many parameter sets, inside one transaction:

```python
import sqlite3

rows = [{"id": i, "name": f"user{i}", "plan": "free" if i % 2 else "pro"} for i in range(1, 6)]
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, plan TEXT)")
with conn:
    cur = conn.executemany("INSERT INTO customers VALUES (:id, :name, :plan)", rows)
print(cur.rowcount, "rows inserted")
```

Add `INSERT OR IGNORE` (or `ON CONFLICT DO NOTHING`) when the batch may contain keys that already exist, so re-running a load does not crash.

## IN lists

A placeholder stands for **one value**, so you cannot pass a list to `IN ?`. Generate one `?` per item and join them. The *text you are building contains only question marks*, never data, so this is safe:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (id INTEGER)")
conn.executemany("INSERT INTO t VALUES (?)", [(i,) for i in range(10)])

ids = [2, 5, 7]
marks = ", ".join("?" * len(ids))
sql = f"SELECT id FROM t WHERE id IN ({marks}) ORDER BY id"
print(sql)
print(conn.execute(sql, ids).fetchall())
```

Handle the empty list explicitly: `IN ()` is a syntax error in most databases, so return early.

## What cannot be a parameter: identifiers

Table names, column names and `ASC`/`DESC` are part of the statement's structure, so `?` does not work for them. Use an **allowlist**:

```python
ALLOWED_SORT = {"id", "name", "plan"}

def order_clause(column: str, direction: str) -> str:
    if column not in ALLOWED_SORT:
        raise ValueError(f"cannot sort by {column!r}")
    if direction.lower() not in {"asc", "desc"}:
        raise ValueError("direction must be asc or desc")
    return f"ORDER BY {column} {direction.upper()}"

print(order_clause("name", "desc"))
try:
    order_clause("name; DROP TABLE customers", "asc")
except ValueError as exc:
    print("rejected:", exc)
```

Anything that comes from outside your code and lands in SQL text must pass through a fixed set of known-good values.

## Common mistakes

- `sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 7 supplied.` You passed `("O'Brien")` (a string) instead of `("O'Brien",)`.
- Putting quotes around a placeholder: `'?'` is a literal question mark, not a parameter.
- Using `IN ?` with a list: `sqlite3.ProgrammingError: Error binding parameter 1: type 'list' is not supported`.
- Using an f-string "just for the table name" with a value you got from a request or file. Allowlist it.
- Forgetting that `executemany` with a generator is fine, but an empty batch does nothing silently.

## What to take away

1. Never put data into SQL text. Use `?` or `:name` and pass values separately.
2. A single value needs a tuple with a trailing comma.
3. `executemany` plus one transaction is the standard bulk load; add `OR IGNORE` for re-runs.
4. For `IN`, generate exactly one `?` per item, and guard the empty list.
5. Identifiers cannot be parameters: validate them against an allowlist.
