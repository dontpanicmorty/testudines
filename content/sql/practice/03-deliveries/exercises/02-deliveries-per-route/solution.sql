SELECT route_id, COUNT(*) AS delivery_count FROM deliveries_info GROUP BY route_id ORDER BY route_id;
