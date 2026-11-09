CREATE OR REPLACE TABLE enrollments (
    id INTEGER,
    year INTEGER,
    studentId INTEGER,
    courseId INTEGER,
    grade_letter VARCHAR
);
INSERT INTO enrollments VALUES
 (10, 2015, 1, 100, 'A'),
 (25, 1999, 2, 100, 'B'),
 (45, 1999, 3, 101, 'C'),
 (60, 2000, 4, 101, 'A'),
 (80, 1999, 5, 102, 'B'),
 (95, 2015, 6, 102, 'A'),
 (120, 2016, 7, 100, 'B'),
 (150, 2016, 8, 101, 'A'),
 (155, 2014, 1, 101, 'C'),
 (160, 2015, 1, 102, 'B'),
 (170, 2016, 3, 100, 'B');
