`orders` is a DataFrame with `order_id`, `customer_id`, `status` and `amount`.

Write `paid_totals(orders)` returning a new DataFrame with columns `customer_id` and `total` (the sum of `amount` over rows whose `status` is `"paid"`), sorted by `total` descending then `customer_id` ascending, with a clean `0..n-1` index. Do not modify the input.

SQL: `SELECT customer_id, SUM(amount) AS total FROM orders WHERE status = 'paid' GROUP BY customer_id ORDER BY total DESC, customer_id`.

```python
paid_totals(orders).to_dict("records")   # [{'customer_id': 10, 'total': 75.5}, ...]
```
