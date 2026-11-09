SELECT delivery_id, delivery_date, CASE DAYOFWEEK(delivery_date) WHEN 1 THEN 'Monday' WHEN 4 THEN 'Thursday' END AS cycle_day FROM deliveries_info ORDER BY delivery_id;
