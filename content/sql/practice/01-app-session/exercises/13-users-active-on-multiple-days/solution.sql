SELECT userId, COUNT(DISTINCT sessionDate) AS active_days FROM sessions GROUP BY userId HAVING COUNT(DISTINCT sessionDate) > 1 ORDER BY userId;
