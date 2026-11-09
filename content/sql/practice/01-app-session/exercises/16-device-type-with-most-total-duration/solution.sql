SELECT deviceType, SUM(duration) AS total_duration FROM sessions GROUP BY deviceType ORDER BY total_duration DESC LIMIT 1;
