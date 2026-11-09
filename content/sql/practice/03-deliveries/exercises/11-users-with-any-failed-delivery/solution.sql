SELECT DISTINCT user_id FROM deliveries_info WHERE user_id IN (SELECT user_id FROM deliveries_info WHERE delivery_success_flag = false) ORDER BY user_id;
