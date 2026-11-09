`rows_as_dicts(cur)` should convert the results of an executed cursor into a list of dicts keyed by **lower-case** column name (Snowflake returns upper-case names). Statements without a result set (`cur.description is None`, such as an `INSERT`) give `[]`.

Right now a query returning three different orders gives back three identical dicts, all equal to the last order. Fix it.

```python
rows_as_dicts(cur)   # [{"order_id": 1, "status": "open"}, {"order_id": 2, "status": "shipped"}]
```
