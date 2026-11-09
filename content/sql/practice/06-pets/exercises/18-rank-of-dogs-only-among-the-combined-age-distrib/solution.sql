WITH combined AS (
  SELECT name, age, 'dog' AS pet_type FROM dogs
  UNION ALL
  SELECT name, age, 'cat' FROM cats
),
ranked AS (
  SELECT name, age, pet_type, ROUND(PERCENT_RANK() OVER (ORDER BY age), 2) AS pct_rank FROM combined
)
SELECT name, age, pct_rank FROM ranked WHERE pet_type = 'dog' ORDER BY age DESC;
