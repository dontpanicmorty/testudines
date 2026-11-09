SELECT grade, gpa, DENSE_RANK() OVER (PARTITION BY grade ORDER BY gpa DESC) AS gpa_dense_rank FROM students ORDER BY grade, gpa_dense_rank;
