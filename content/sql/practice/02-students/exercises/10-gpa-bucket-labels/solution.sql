SELECT firstName, gpa, CASE WHEN gpa >= 3.5 THEN 'high' WHEN gpa >= 3.0 THEN 'mid' ELSE 'low' END AS gpa_band FROM students ORDER BY gpa DESC;
