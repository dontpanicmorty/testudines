Implement the equivalent of:

```sql
SUM(amount) OVER (PARTITION BY customer ORDER BY day ROWS UNBOUNDED PRECEDING) AS running_total,
LAG(amount)  OVER (PARTITION BY customer ORDER BY day) AS prev_amount
```

`add_window_columns(orders)` takes dict rows with `customer`, `day` (ISO date string) and `amount`, and returns **new** dicts (inputs untouched) with `running_total` and `prev_amount` added, sorted by `(customer, day)`. Rows with the same customer and day keep their input order (stable sort). This one is from scratch.

```python
add_window_columns([{"customer": "Ada", "day": "2025-06-02", "amount": 70},
                    {"customer": "Ada", "day": "2025-06-01", "amount": 50}])
# [{"customer": "Ada", "day": "2025-06-01", "amount": 50, "running_total": 50, "prev_amount": None},
#  {"customer": "Ada", "day": "2025-06-02", "amount": 70, "running_total": 120, "prev_amount": 50}]
```
