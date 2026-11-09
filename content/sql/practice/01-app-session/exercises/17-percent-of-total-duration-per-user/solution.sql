SELECT userId,
       SUM(duration) AS total_duration,
       ROUND(100.0 * SUM(duration) / SUM(SUM(duration)) OVER (), 1) AS pct_of_total
FROM sessions
GROUP BY userId
ORDER BY pct_of_total DESC;
