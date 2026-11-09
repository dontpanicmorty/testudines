Implement the lesson's task with pandas.

`top_pandas(orders, items, n)` takes `orders` (list of dicts `order_id, customer_id, status`) and `items` (list of dicts `order_id, quantity, unit_price`) and returns the top `n` customers as a list of `(customer_id, revenue)` tuples: revenue is the sum of `quantity * unit_price` over their **non-cancelled** orders, rounded to 2 decimals, as plain Python `int` / `float`; sorted by revenue descending then `customer_id` ascending. Inputs may be empty lists (then return `[]`).
