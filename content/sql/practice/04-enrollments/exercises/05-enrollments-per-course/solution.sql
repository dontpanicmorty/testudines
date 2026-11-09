SELECT courseId, COUNT(*) AS enrollment_count FROM enrollments GROUP BY courseId ORDER BY courseId;
