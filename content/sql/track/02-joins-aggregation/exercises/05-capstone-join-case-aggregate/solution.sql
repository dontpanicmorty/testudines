SELECT c.region,
       COUNT(DISTINCT c.customer_id) AS customer_count,
       COALESCE(SUM(CASE WHEN o.status='completed' THEN o.amount END),0) AS total_completed_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.region
ORDER BY total_completed_amount DESC;
