SELECT id, firstName, grade, gpa, ROUND(gpa - LEAD(gpa) OVER (PARTITION BY grade ORDER BY gpa DESC), 2) AS gap_to_next FROM students ORDER BY grade, gpa DESC;
