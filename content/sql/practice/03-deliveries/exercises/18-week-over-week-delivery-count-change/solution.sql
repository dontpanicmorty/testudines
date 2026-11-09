WITH weekly AS (
  SELECT delivery_week, COUNT(*) AS delivery_count FROM deliveries_info GROUP BY delivery_week
)
SELECT delivery_week, delivery_count, delivery_count - LAG(delivery_count) OVER (ORDER BY delivery_week) AS change_from_prev
FROM weekly
ORDER BY delivery_week;
