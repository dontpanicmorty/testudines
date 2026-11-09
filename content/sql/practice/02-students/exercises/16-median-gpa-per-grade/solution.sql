SELECT grade, MEDIAN(gpa) AS median_gpa FROM students GROUP BY grade ORDER BY grade;
