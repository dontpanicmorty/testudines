Write `store_readings(db_path, rows)`. `rows` is a list of `(station, bikes)` tuples. Open the SQLite file at `db_path`, create a table named `reading` with columns `station` (text) and `bikes` (integer) if it does not exist, insert every row, make sure the data is saved, and return the number of rows inserted. Calling it again appends more rows.

```python
store_readings("x.db", [("Mill Lane", 4), ("Hill Top", 9)])   # 2
```
