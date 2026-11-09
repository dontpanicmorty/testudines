UPDATE enrollments SET grade_letter = 'A' WHERE id IN (SELECT MAX(id) FROM enrollments GROUP BY studentId);
