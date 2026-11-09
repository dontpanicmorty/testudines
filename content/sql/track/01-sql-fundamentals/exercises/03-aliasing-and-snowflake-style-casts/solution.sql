SELECT order_id, amount::INTEGER AS amount_whole_dollars, order_date::VARCHAR AS order_date_string FROM orders ORDER BY order_id;
