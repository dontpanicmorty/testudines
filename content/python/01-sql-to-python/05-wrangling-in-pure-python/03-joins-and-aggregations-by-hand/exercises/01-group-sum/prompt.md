Write `group_totals(rows, key, value)` returning `{group: {"count": n, "total": sum_of_value}}` for a list of dict rows. Rows where `value` is `None` still count in `count` but add nothing to `total` (like `COUNT(*)` vs `SUM`).

```python
rows = [{"region": "EU", "amt": 50}, {"region": "US", "amt": 20}, {"region": "EU", "amt": None}]
group_totals(rows, "region", "amt")
# {"EU": {"count": 2, "total": 50}, "US": {"count": 1, "total": 20}}
```
