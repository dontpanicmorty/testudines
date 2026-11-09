Write `build_query(table, schema="analytics", limit=None, **filters)` returning a SQL string. (It only builds text; nothing runs.)

- Base: `SELECT * FROM <schema>.<table>`
- Each extra keyword argument becomes an equality filter on a string value, joined with ` AND `, **sorted by column name**: ` WHERE a = 'x' AND b = 'y'`
- If `limit` is not `None`, append ` LIMIT <n>`.

```python
build_query("orders")
# "SELECT * FROM analytics.orders"
build_query("orders", schema="raw", limit=10)
# "SELECT * FROM raw.orders LIMIT 10"
build_query("orders", status="paid", region="EU")
# "SELECT * FROM analytics.orders WHERE region = 'EU' AND status = 'paid'"
```
