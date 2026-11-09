Two functions.

`top_polars(orders, items, n)`: the lesson's task in polars. `orders` are dicts `order_id, customer_id, status`; `items` are dicts `order_id, quantity, unit_price`. Return the top `n` customers as `(customer_id, revenue)` tuples (plain `int`/`float`, revenue rounded to 2 decimals) from non-cancelled orders, sorted by revenue descending then `customer_id` ascending. Empty inputs give `[]`.

`normalise(rows)`: takes the output of *any* tool, an iterable of `(customer_id, revenue)` pairs whose values may be numpy or other numeric types and may be in any tie order, and returns a list of plain `(int, float)` tuples with revenue rounded to 2 decimals, sorted by revenue descending then `customer_id` ascending. Use it to assert that tools agree: `normalise(a) == normalise(b)`.
