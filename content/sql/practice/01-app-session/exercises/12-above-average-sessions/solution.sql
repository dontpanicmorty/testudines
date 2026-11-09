SELECT id, userId, duration FROM sessions WHERE duration > (SELECT AVG(duration) FROM sessions) ORDER BY duration DESC;
