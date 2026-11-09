Write `index_paid(orders)` returning a dict mapping `order_id` to `amount` for orders whose `status` (case-insensitive, stripped) is `"paid"`, using a dict comprehension. If an `order_id` appears twice, the later row wins.

Also write `line_numbers(lines)` returning a list of `"<n>: <line>"` strings starting at 1, using `enumerate`.

```python
orders = [{"order_id": "a", "status": "Paid ", "amount": 5.0},
          {"order_id": "b", "status": "refunded", "amount": 9.0},
          {"order_id": "a", "status": "paid", "amount": 7.0}]
index_paid(orders)            # {"a": 7.0}
line_numbers(["x", "y"])      # ["1: x", "2: y"]
```
