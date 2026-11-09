WITH points AS (
  SELECT courseId, studentId, CASE grade_letter WHEN 'A' THEN 4 WHEN 'B' THEN 3 WHEN 'C' THEN 2 END AS pts
  FROM enrollments
)
SELECT courseId, studentId, ROUND(PERCENT_RANK() OVER (PARTITION BY courseId ORDER BY pts), 2) AS pct_rank
FROM points
ORDER BY courseId, pct_rank DESC;
