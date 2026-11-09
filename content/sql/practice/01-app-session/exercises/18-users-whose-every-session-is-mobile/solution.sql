SELECT DISTINCT userId FROM sessions s1 WHERE NOT EXISTS (SELECT 1 FROM sessions s2 WHERE s2.userId = s1.userId AND s2.deviceType != 'mobile') ORDER BY userId;
