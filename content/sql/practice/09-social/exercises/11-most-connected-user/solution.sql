SELECT u.name, COUNT(*) AS friend_count FROM users u JOIN friends f ON u.id = f.user1 OR u.id = f.user2 GROUP BY u.name ORDER BY friend_count DESC LIMIT 1;
