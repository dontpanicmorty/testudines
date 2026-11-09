SELECT userId, ROUND(100.0 * SUM(CASE WHEN deviceType = 'mobile' THEN 1 ELSE 0 END) / COUNT(*), 1) AS mobile_pct FROM sessions GROUP BY userId ORDER BY userId;
