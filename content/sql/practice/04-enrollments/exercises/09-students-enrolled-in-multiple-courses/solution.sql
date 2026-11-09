SELECT studentId, COUNT(DISTINCT courseId) AS course_count FROM enrollments GROUP BY studentId HAVING COUNT(DISTINCT courseId) > 1 ORDER BY studentId;
