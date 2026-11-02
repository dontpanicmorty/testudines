Write `load_rows(conn, table, columns, rows, batch_size=1000)` that inserts rows through a DB-API-style connection (`conn.cursor()`, `cur.executemany(sql, seq_of_tuples)`, `conn.commit()`, `conn.rollback()`):

- SQL is `INSERT INTO <table> (<col1>, <col2>) VALUES (%s, %s)`, one `%s` per column, columns joined with `, `.
- `rows` is an iterable of **dicts**; send each batch as a list of tuples in `columns` order. Use at most `batch_size` rows per `executemany` call, and don't hold more than one batch in memory.
- Commit **once**, after all batches succeeded. If any batch raises, roll back and re-raise the original exception, with no commit.
- Close the cursor in all cases. Return the number of rows loaded.

```python
load_rows(conn, "orders", ["order_id", "status"], [{"order_id": 1, "status": "open", "x": 0}], batch_size=500)  # 1
```
