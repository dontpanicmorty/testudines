Late-arriving corrections mean a table can hold several versions of one record. Write `latest_per_key(con, table, key, ts_col)` for a DuckDB connection `con` (DuckDB's `con.execute(sql).fetchall()` and `con.description` work like a DB-API cursor).

It returns a list of dicts (column name to value, all columns of the table) with only the **most recent** row for each `key`, where recent means the greatest `ts_col`. Order the result by `key` ascending. If two versions of a key share the same `ts_col`, either may win, but only one row per key is returned. Validate `table`, `key` and `ts_col` as simple identifiers (`[A-Za-z_][A-Za-z0-9_]*`), otherwise raise `ValueError`.

```python
latest_per_key(con, "customers", "id", "updated_at")
# [{"id": 1, "email": "new@x.test", "updated_at": 2}, {"id": 2, ...}]
```
