WITH yearly AS (
  SELECT year, COUNT(*) AS enrollment_count FROM enrollments GROUP BY year
)
SELECT year, enrollment_count, enrollment_count - LAG(enrollment_count) OVER (ORDER BY year) AS change_from_prev
FROM yearly
ORDER BY year;
