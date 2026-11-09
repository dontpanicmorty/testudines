`orders` is a list of dicts with `status` and `amount`. This is `SELECT status, COUNT(*), SUM(amount) ... GROUP BY status` in plain Python.

Write `summarise(orders)` returning a dict mapping each status to `{"count": n, "total": t}`, with `total` rounded to 2 decimals. Use the dict-building pattern from the lesson (no imports needed).

```python
orders = [
    {"status": "paid", "amount": 10.5},
    {"status": "paid", "amount": 4.25},
    {"status": "refunded", "amount": 3.0},
]
summarise(orders)
# {"paid": {"count": 2, "total": 14.75}, "refunded": {"count": 1, "total": 3.0}}
summarise([])  # {}
```
