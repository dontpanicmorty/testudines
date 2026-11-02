Write `build_merge_sql(table, staging, keys, columns)` returning the MERGE statement that upserts rows from a staging table into a target. Whitespace and keyword case do not matter to the tests, but the structure and column order do:

```
MERGE INTO <table> AS tgt USING <staging> AS src
ON tgt.<k1> = src.<k1> AND tgt.<k2> = src.<k2>
WHEN MATCHED THEN UPDATE SET tgt.<c> = src.<c>, ...
WHEN NOT MATCHED THEN INSERT (<columns>) VALUES (src.<c>, ...)
```

- `UPDATE SET` lists the non-key columns, in `columns` order.
- If there are no non-key columns, omit the `WHEN MATCHED` clause.
- `columns` must be non-empty and `keys` must be a non-empty subset of it, otherwise raise `ValueError`.
- No trailing semicolon.

```python
build_merge_sql("orders", "orders_stg", ["order_id"], ["order_id", "status"])
```
