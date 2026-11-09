SELECT userId, COUNT(*) AS session_count FROM sessions GROUP BY userId ORDER BY userId;
