A finance export is wide: one row per product, one column per month. Warehouses want it long (an UNPIVOT).

Write `unpivot(rows, id_field="product")` that turns each wide row into one record per month, `{"product": ..., "month": ..., "revenue": float}`. Skip cells that are `None` or `""`. Keep row order, then column order within each row.

```python
rows = [{"product": "A", "2024-01": "10.5", "2024-02": None},
        {"product": "B", "2024-01": "3", "2024-02": "4.25"}]
unpivot(rows)
# [{"product": "A", "month": "2024-01", "revenue": 10.5},
#  {"product": "B", "month": "2024-01", "revenue": 3.0},
#  {"product": "B", "month": "2024-02", "revenue": 4.25}]
```

The id column name is a parameter: the output key is always `"product"` only when `id_field="product"`; otherwise use the `id_field` name as the key.
