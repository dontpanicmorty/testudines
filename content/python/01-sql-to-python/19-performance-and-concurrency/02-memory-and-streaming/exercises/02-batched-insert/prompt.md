`load_rows(conn, rows, batch_size)` inserts `(id, kind)` tuples into the table `events(id INTEGER, kind TEXT)` and returns the number of rows inserted. `rows` may be a generator producing millions of rows.

It works, but the process's memory grows with the size of the input and nothing is written until the very end. It should hold **at most one batch** of rows at a time, insert each batch with `executemany`, and commit per batch.

```python
conn = sqlite3.connect(":memory:")
conn.execute("create table events(id integer, kind text)")
load_rows(conn, ((i, "click") for i in range(10)), batch_size=4)   # 10
```

Fix `solution.py` without changing its signature or return value.
