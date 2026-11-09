SELECT name FROM users WHERE id NOT IN (SELECT user1 FROM friends UNION SELECT user2 FROM friends) ORDER BY name;
