WITH f_all AS (SELECT user1 AS a, user2 AS b FROM friends UNION ALL SELECT user2, user1 FROM friends)
SELECT u.name, COUNT(f.b) AS friend_count
FROM users u LEFT JOIN f_all f ON u.id = f.a
GROUP BY u.name
ORDER BY friend_count DESC, u.name;
