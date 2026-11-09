`data_dir` contains `orders.csv(order_id, customer_id, placed_at, status)` and `order_items.csv(order_id, product_id, quantity, unit_price)`.

Write `top_customers(data_dir, n)` that uses DuckDB to return the `n` customers with the highest revenue, as a list of `(customer_id, revenue)` tuples. Revenue is the sum of `quantity * unit_price` over their **non-cancelled** orders, rounded to 2 decimals. Order by revenue descending, then `customer_id` ascending.

```python
top_customers("datasets", 3)   # [(42, 1234.5), (7, 1200.0), (13, 999.99)]
```
