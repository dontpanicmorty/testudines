Write `enrich_orders(orders, customers)`.

`orders` has `order_id`, `customer_id`, `amount`. `customers` has `customer_id`, `first_name`, `last_name`.

Return one row per order (even if the customer is unknown) with columns `order_id`, `customer_id`, `amount`, `full_name` (`"first last"`, missing when unknown), in the original order of `orders`. If `customers` contains a duplicated `customer_id`, let pandas raise `pd.errors.MergeError` rather than returning duplicated orders.

SQL: `SELECT o.order_id, o.customer_id, o.amount, c.first_name || ' ' || c.last_name AS full_name FROM orders o LEFT JOIN customers c USING (customer_id)`.
