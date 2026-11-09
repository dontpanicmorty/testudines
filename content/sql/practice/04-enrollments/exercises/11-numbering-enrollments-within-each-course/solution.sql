SELECT courseId, studentId, id, ROW_NUMBER() OVER (PARTITION BY courseId ORDER BY id) AS rn FROM enrollments ORDER BY courseId, rn;
