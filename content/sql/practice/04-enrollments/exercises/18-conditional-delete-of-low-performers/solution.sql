DELETE FROM enrollments WHERE grade_letter IS NULL AND studentId NOT IN (SELECT studentId FROM enrollments WHERE grade_letter = 'A');
