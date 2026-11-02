Write `top_customers(orders_csv, items_csv, n)` that returns a Polars **`LazyFrame`** (not collected) with columns `customer_id` and `revenue`.

- `orders_csv` has `order_id,customer_id,placed_at,status`; `items_csv` has `order_id,product_id,quantity,unit_price`.
- Only orders with status `completed` or `shipped` count.
- `revenue` = sum of `quantity * unit_price` per customer, rounded to 2 decimals.
- Sorted by `revenue` descending, ties by `customer_id` ascending, limited to `n` rows.
- Use `pl.scan_csv` so nothing is read until the caller runs `.collect()`.

```python
top_customers("orders.csv", "order_items.csv", 5).collect()
```
