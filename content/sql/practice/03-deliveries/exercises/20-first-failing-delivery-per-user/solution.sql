SELECT * FROM deliveries_info WHERE delivery_success_flag = false QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY delivery_date) = 1 ORDER BY user_id;
