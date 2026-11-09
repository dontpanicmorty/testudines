`orders.csv` has `order_id, customer_id, placed_at, status` (`placed_at` like `2025-03-22 22:50:00`) and `order_items.csv` has `order_id, product_id, quantity, unit_price`.

Write `daily_revenue(orders_path, items_path)` using **lazy** polars (`scan_csv`) that returns a DataFrame with columns `day` (string `YYYY-MM-DD`) and `revenue` (sum of `quantity * unit_price` over non-cancelled orders, rounded to 2 decimals), sorted by `day` ascending. Days with no revenue do not appear.
