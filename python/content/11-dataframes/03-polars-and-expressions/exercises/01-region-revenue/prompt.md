`orders` is a polars DataFrame with `region`, `status`, `amount`. Write `region_revenue(orders)` returning a polars DataFrame with columns `region`, `n_orders`, `total`, computed over rows where `status != "cancelled"`, sorted by `total` descending then `region` ascending.

SQL: `SELECT region, COUNT(*) AS n_orders, SUM(amount) AS total FROM orders WHERE status <> 'cancelled' GROUP BY region ORDER BY total DESC, region`.
