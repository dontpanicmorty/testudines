SELECT id, firstName, gpa, ROUND(PERCENT_RANK() OVER (ORDER BY gpa), 2) AS pct_rank FROM students ORDER BY gpa DESC;
