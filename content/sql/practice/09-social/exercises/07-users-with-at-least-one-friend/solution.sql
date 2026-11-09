SELECT name FROM users WHERE id IN (SELECT user1 FROM friends UNION SELECT user2 FROM friends) ORDER BY name;
