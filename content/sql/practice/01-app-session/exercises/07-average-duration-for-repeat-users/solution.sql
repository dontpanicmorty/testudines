SELECT userId, AVG(duration) AS avg_duration FROM sessions GROUP BY userId HAVING COUNT(*) > 1 ORDER BY userId;
