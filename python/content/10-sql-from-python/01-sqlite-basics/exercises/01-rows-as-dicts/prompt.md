Write `query_dicts(conn, sql)` that runs a SELECT on an open sqlite3 connection and returns the rows as a **list of dicts** keyed by column name. It must not leave `conn.row_factory` changed for the caller (restore what it was).

```python
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (id INTEGER, name TEXT)")
conn.execute("INSERT INTO t VALUES (1, 'Ada')")
query_dicts(conn, "SELECT id, name FROM t")   # [{'id': 1, 'name': 'Ada'}]
```
