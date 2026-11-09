SELECT id, userId, sessionDate, duration, SUM(duration) OVER (PARTITION BY userId ORDER BY sessionDate) AS running_total FROM sessions ORDER BY userId, sessionDate;
