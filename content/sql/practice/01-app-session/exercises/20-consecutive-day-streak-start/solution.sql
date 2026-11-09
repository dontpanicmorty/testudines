SELECT userId, sessionDate,
       sessionDate - (ROW_NUMBER() OVER (PARTITION BY userId ORDER BY sessionDate) * INTERVAL 1 DAY) AS streak_group
FROM sessions
ORDER BY userId, sessionDate;
