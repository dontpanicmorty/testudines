WITH combined AS (
  SELECT breed, 'dog' AS pet_type FROM dogs
  UNION ALL
  SELECT breed, 'cat' FROM cats
)
SELECT breed, ROUND(100.0 * SUM(CASE WHEN pet_type = 'dog' THEN 1 ELSE 0 END) / COUNT(*), 1) AS dog_pct
FROM combined
GROUP BY breed
HAVING COUNT(DISTINCT pet_type) = 2
ORDER BY breed;
