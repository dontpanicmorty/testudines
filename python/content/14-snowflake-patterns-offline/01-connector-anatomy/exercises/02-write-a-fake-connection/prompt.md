Build the test double you will reuse for warehouse code: `FakeConnection` and `FakeCursor`.

`FakeConnection(script)`: `script` is a list of result sets; each result set is a list of dict rows (all rows of one set share the same keys).

- `conn.executed` is a list of `(sql, params)` tuples, one per `execute` call across all cursors.
- `conn.cursor()` returns a `FakeCursor`. `conn.close()` sets `conn.closed = True`; `conn.commit()` increments `conn.commits`. The connection supports `with`, closing on exit.

`FakeCursor`:

- `execute(sql, params=None)` records the call, takes the **next** result set from the script (raise `RuntimeError("no scripted result for: <sql>")` if none is left) and returns `self`.
- `description` is `None` before any execute or when the result set is empty; otherwise a list of 7-tuples whose first item is the column name (upper-cased, as Snowflake does).
- `fetchone()` returns the next row as a tuple (values in key order) or `None`; `fetchmany(n)` returns up to `n` tuples; `fetchall()` returns all remaining tuples. `rowcount` is the number of rows in the current result set.
- `close()` sets `closed = True`; the cursor supports `with`.

```python
conn = FakeConnection([[{"id": 1, "name": "Ada"}, {"id": 2, "name": "Linus"}]])
cur = conn.cursor(); cur.execute("SELECT id, name FROM c")
cur.fetchone()    # (1, "Ada")
cur.description[0][0]   # "ID"
```
