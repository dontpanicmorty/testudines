WITH points AS (
  SELECT id, studentId, grade_letter, CASE grade_letter WHEN 'A' THEN 4 WHEN 'B' THEN 3 WHEN 'C' THEN 2 END AS pts
  FROM enrollments
),
with_prev AS (
  SELECT id, studentId, grade_letter, pts,
         LAG(grade_letter) OVER (PARTITION BY studentId ORDER BY id) AS prev_grade,
         LAG(pts) OVER (PARTITION BY studentId ORDER BY id) AS prev_pts
  FROM points
)
SELECT studentId, id, grade_letter, prev_grade
FROM with_prev
WHERE prev_pts IS NOT NULL AND pts > prev_pts
ORDER BY studentId, id;
