SELECT s.id, s.firstName, s.lastName FROM students s WHERE NOT EXISTS (SELECT 1 FROM students s2 WHERE s2.firstName = s.firstName AND s2.grade != s.grade AND s2.id != s.id) ORDER BY s.id;
