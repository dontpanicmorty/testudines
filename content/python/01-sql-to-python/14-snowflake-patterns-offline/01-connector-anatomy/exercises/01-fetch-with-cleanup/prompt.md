Write two helpers that talk to any DB-API-style connection (`conn.cursor()`, `cur.execute(sql, params)`, `cur.fetchall()`, `cur.fetchone()`):

- `fetch_all(conn, sql, params=None)` returns the list of row tuples. The cursor must be closed afterwards, **even if `execute` raises**.
- `scalar(conn, sql, params=None, default=None)` returns the first column of the first row, or `default` if there are no rows. Same cleanup rule.

```python
fetch_all(conn, "SELECT id, name FROM customers WHERE region = %(r)s", {"r": "EU"})
scalar(conn, "SELECT MAX(placed_at) FROM orders", default="1970-01-01")
```

Cursors support `with`.
