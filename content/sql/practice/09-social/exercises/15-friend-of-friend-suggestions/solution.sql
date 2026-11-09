WITH f_all AS (SELECT user1 AS a, user2 AS b FROM friends UNION SELECT user2, user1 FROM friends)
SELECT DISTINCT u.name
FROM f_all direct
JOIN f_all indirect ON direct.b = indirect.a
JOIN users u ON u.id = indirect.b
WHERE direct.a = 1
  AND indirect.b != 1
  AND NOT EXISTS (SELECT 1 FROM f_all fx WHERE fx.a = 1 AND fx.b = indirect.b)
ORDER BY u.name;
