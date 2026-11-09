SELECT route_id, ROUND(100.0 * SUM(CASE WHEN delivery_success_flag THEN 1 ELSE 0 END) / COUNT(*), 1) AS success_rate FROM deliveries_info GROUP BY route_id ORDER BY route_id;
