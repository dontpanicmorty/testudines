SELECT id, firstName, grade, gpa, RANK() OVER (PARTITION BY grade ORDER BY gpa DESC) AS grade_rank FROM students ORDER BY grade, grade_rank;
