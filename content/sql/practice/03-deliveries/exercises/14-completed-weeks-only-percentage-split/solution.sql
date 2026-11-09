WITH labeled AS (
  SELECT delivery_week,
         CASE DAYOFWEEK(delivery_date) WHEN 1 THEN 'Monday' WHEN 4 THEN 'Thursday' END AS cycle_day
  FROM deliveries_info
  WHERE delivery_week < (SELECT MAX(delivery_week) FROM deliveries_info)
)
SELECT delivery_week,
       ROUND(100.0 * SUM(CASE WHEN cycle_day = 'Monday' THEN 1 ELSE 0 END) / COUNT(*), 1) AS monday_pct,
       ROUND(100.0 * SUM(CASE WHEN cycle_day = 'Thursday' THEN 1 ELSE 0 END) / COUNT(*), 1) AS thursday_pct
FROM labeled
GROUP BY delivery_week
ORDER BY delivery_week;
