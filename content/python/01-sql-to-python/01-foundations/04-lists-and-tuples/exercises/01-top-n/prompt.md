`orders` is a list of `(order_id, amount)` tuples. Write `top_n(orders, n)` that returns the `n` largest by amount as a new list, biggest first (`ORDER BY amount DESC LIMIT n`). Ties keep their original order. The input list must not be changed.

```python
orders = [("o1", 50), ("o2", 90), ("o3", 20)]
top_n(orders, 2)   # [("o2", 90), ("o1", 50)]
top_n(orders, 10)  # all three, sorted
```
