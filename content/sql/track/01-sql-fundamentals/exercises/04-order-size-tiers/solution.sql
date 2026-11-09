SELECT order_id, amount, CASE WHEN amount >= 100 THEN 'large' WHEN amount >= 50 THEN 'medium' ELSE 'small' END AS business_tier FROM orders ORDER BY order_id;
