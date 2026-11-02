Write `open_db(path)` that every job in a pipeline can call to get its database connection. It must:

1. connect to the SQLite file at `path`,
2. set `row_factory` so rows can be read by column name,
3. turn on foreign key enforcement,
4. create (if missing) these tables, safely callable many times:
   - `runs(id INTEGER PRIMARY KEY, started TEXT NOT NULL)`
   - `run_rows(id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL REFERENCES runs(id), payload TEXT)`
5. return the connection.

```python
conn = open_db("pipeline.db")
conn.execute("INSERT INTO runs (started) VALUES ('2025-01-01')")
conn.commit()
conn.execute("SELECT started FROM runs").fetchone()["started"]   # '2025-01-01'
```
