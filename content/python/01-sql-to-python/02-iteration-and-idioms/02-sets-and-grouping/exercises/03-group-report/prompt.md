Write `revenue_report(orders)` from scratch. Each order is a dict with `region`, `plan` and `amount`.

Return a list of dicts, one per `(region, plan)` pair, sorted by region then plan, each shaped:

`{"region": ..., "plan": ..., "orders": <count>, "revenue": <sum rounded to 2>, "avg": <mean rounded to 2>}`

```python
orders = [
  {"region": "EU", "plan": "pro", "amount": 10.0},
  {"region": "EU", "plan": "pro", "amount": 5.0},
  {"region": "US", "plan": "free", "amount": 1.0},
]
revenue_report(orders)
# [{"region": "EU", "plan": "pro", "orders": 2, "revenue": 15.0, "avg": 7.5},
#  {"region": "US", "plan": "free", "orders": 1, "revenue": 1.0, "avg": 1.0}]
```
