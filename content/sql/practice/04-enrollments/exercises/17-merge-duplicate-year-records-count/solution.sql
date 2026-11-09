SELECT studentId, courseId, COUNT(*) AS row_count FROM enrollments GROUP BY studentId, courseId HAVING COUNT(*) > 1 ORDER BY studentId;
