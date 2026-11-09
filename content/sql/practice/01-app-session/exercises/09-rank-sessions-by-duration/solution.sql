SELECT id, userId, duration, RANK() OVER (ORDER BY duration DESC) AS duration_rank FROM sessions ORDER BY duration_rank;
