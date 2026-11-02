Implement the task from the lesson twice.

`top_python(orders, items, n)` and `top_duckdb(orders, items, n)` take:

- `orders`: list of dicts `order_id, customer_id, status`
- `items`: list of dicts `order_id, quantity, unit_price`

and return the top `n` customers as a list of `(customer_id, revenue)` tuples: revenue is the sum of `quantity * unit_price` over their **non-cancelled** orders, rounded to 2 decimals (Python `int` and `float` types); sorted by revenue descending then `customer_id` ascending. Customers with no non-cancelled items are not listed. Both must give identical results.
