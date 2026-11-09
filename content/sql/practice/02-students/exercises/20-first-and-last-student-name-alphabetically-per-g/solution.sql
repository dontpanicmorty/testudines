SELECT grade, MIN(lastName) AS first_alpha, MAX(lastName) AS last_alpha FROM students GROUP BY grade ORDER BY grade;
