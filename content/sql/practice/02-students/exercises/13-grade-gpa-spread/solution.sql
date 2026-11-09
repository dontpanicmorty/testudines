SELECT grade, ROUND(MAX(gpa) - MIN(gpa), 2) AS gpa_spread FROM students GROUP BY grade ORDER BY grade;
