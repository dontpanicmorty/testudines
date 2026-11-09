UPDATE enrollments SET grade_letter = CASE WHEN grade_letter = 'C' THEN 'B' ELSE 'A' END WHERE id BETWEEN 20 AND 100;
