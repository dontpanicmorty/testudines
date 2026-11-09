SELECT c.first_name, c.last_name, o.order_id, o.amount FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.status = 'completed' ORDER BY c.customer_id, o.order_id;
