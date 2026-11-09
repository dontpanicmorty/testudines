SELECT route_id, COUNT(DISTINCT user_id) AS distinct_users FROM deliveries_info GROUP BY route_id ORDER BY route_id;
