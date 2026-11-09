WITH route_rates AS (
  SELECT route_id, ROUND(100.0 * SUM(CASE WHEN delivery_success_flag THEN 1 ELSE 0 END) / COUNT(*), 1) AS success_rate
  FROM deliveries_info
  GROUP BY route_id
)
SELECT route_id, success_rate, RANK() OVER (ORDER BY success_rate DESC) AS reliability_rank
FROM route_rates
ORDER BY reliability_rank;
