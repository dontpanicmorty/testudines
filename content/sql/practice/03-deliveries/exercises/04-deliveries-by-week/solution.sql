SELECT delivery_week, COUNT(*) AS delivery_count FROM deliveries_info GROUP BY delivery_week ORDER BY delivery_week;
