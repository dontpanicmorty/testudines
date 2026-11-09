WITH flagged AS (
  SELECT *, SUM(CASE WHEN NOT delivery_success_flag THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY delivery_date) AS failure_group
  FROM deliveries_info
)
SELECT delivery_id, delivery_date, delivery_success_flag,
       CASE WHEN delivery_success_flag THEN ROW_NUMBER() OVER (PARTITION BY user_id, failure_group ORDER BY delivery_date) ELSE 0 END AS streak
FROM flagged
ORDER BY user_id, delivery_date;
