SELECT userId, MIN(sessionDate) AS first_session FROM sessions GROUP BY userId ORDER BY userId;
