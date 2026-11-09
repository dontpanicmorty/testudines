SELECT id, firstName, grade, gpa FROM students QUALIFY ROW_NUMBER() OVER (PARTITION BY grade ORDER BY gpa DESC) <= 2 ORDER BY grade, gpa DESC;
