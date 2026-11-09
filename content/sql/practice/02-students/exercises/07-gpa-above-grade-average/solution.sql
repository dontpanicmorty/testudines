SELECT s.id, s.firstName, s.grade, s.gpa FROM students s WHERE s.gpa > (SELECT AVG(s2.gpa) FROM students s2 WHERE s2.grade = s.grade) ORDER BY s.grade, s.gpa DESC;
