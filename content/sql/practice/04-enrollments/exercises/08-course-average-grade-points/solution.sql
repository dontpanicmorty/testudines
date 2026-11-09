SELECT courseId, ROUND(AVG(CASE grade_letter WHEN 'A' THEN 4 WHEN 'B' THEN 3 WHEN 'C' THEN 2 END), 2) AS avg_points FROM enrollments GROUP BY courseId ORDER BY courseId;
