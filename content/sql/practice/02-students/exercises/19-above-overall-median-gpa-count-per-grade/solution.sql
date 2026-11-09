SELECT grade, COUNT(*) AS above_median_count FROM students WHERE gpa > (SELECT MEDIAN(gpa) FROM students) GROUP BY grade ORDER BY grade;
