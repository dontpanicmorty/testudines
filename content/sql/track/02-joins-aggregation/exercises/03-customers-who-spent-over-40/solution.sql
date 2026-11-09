SELECT customer_id, SUM(amount) AS total_spent FROM orders WHERE status='completed' GROUP BY customer_id HAVING SUM(amount) > 40 ORDER BY total_spent DESC;
