SELECT userId, SUM(duration) AS total_duration FROM sessions GROUP BY userId ORDER BY total_duration DESC;
