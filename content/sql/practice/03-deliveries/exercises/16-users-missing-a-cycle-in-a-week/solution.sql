WITH labeled AS (
  SELECT user_id, delivery_week,
         CASE DAYOFWEEK(delivery_date) WHEN 1 THEN 'Monday' WHEN 4 THEN 'Thursday' END AS cycle_day
  FROM deliveries_info
)
SELECT DISTINCT l1.user_id, l1.delivery_week
FROM labeled l1
WHERE l1.cycle_day = 'Monday'
  AND NOT EXISTS (
    SELECT 1 FROM labeled l2
    WHERE l2.user_id = l1.user_id AND l2.delivery_week = l1.delivery_week AND l2.cycle_day = 'Thursday'
  )
ORDER BY l1.delivery_week, l1.user_id;
