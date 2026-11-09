SELECT user_id, delivery_week, COUNT(*) AS delivery_count FROM deliveries_info GROUP BY user_id, delivery_week ORDER BY user_id, delivery_week;
