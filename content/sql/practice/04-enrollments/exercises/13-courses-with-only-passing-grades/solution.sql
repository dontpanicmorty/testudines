SELECT DISTINCT courseId FROM enrollments e1 WHERE NOT EXISTS (SELECT 1 FROM enrollments e2 WHERE e2.courseId = e1.courseId AND e2.grade_letter = 'F') ORDER BY courseId;
