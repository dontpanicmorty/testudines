SELECT grade_letter, COUNT(*) AS letter_count FROM enrollments GROUP BY grade_letter ORDER BY grade_letter;
