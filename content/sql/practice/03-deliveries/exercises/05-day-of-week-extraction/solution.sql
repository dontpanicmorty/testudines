SELECT delivery_id, delivery_date, DAYOFWEEK(delivery_date) AS dow FROM deliveries_info ORDER BY delivery_id;
