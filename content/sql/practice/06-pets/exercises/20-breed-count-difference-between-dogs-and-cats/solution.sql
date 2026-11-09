WITH d AS (SELECT breed, COUNT(*) AS dog_count FROM dogs GROUP BY breed),
     c AS (SELECT breed, COUNT(*) AS cat_count FROM cats GROUP BY breed)
SELECT COALESCE(d.breed, c.breed) AS breed, COALESCE(d.dog_count, 0) AS dog_count, COALESCE(c.cat_count, 0) AS cat_count
FROM d FULL OUTER JOIN c ON d.breed = c.breed
ORDER BY breed;
