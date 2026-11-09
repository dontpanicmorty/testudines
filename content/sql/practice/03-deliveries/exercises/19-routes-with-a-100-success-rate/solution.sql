SELECT route_id FROM deliveries_info GROUP BY route_id HAVING SUM(CASE WHEN delivery_success_flag THEN 0 ELSE 1 END) = 0 ORDER BY route_id;
