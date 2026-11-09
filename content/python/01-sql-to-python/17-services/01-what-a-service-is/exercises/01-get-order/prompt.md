A tiny order service keeps orders in a dict keyed by integer `order_id`. The URL gives you the id as **text**.

Write `get_order(orders, raw_id)` that models a `GET /orders/{id}` handler and returns `(status, body)`:

- id is not a valid integer: `(400, {"error": "invalid order id"})`
- id valid but missing: `(404, {"error": "order 7 not found"})` (with the real id)
- found: `(200, <the order dict>)`

```python
orders = {1001: {"order_id": 1001, "status": "shipped"}}
get_order(orders, "1001")   # (200, {"order_id": 1001, "status": "shipped"})
get_order(orders, "abc")    # (400, {"error": "invalid order id"})
get_order(orders, "7")      # (404, {"error": "order 7 not found"})
```

Edit `solution.py`, then press **Check**.
