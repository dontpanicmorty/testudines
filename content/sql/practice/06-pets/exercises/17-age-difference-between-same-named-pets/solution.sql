SELECT d.name, ABS(d.age - c.age) AS age_diff FROM dogs d JOIN cats c ON d.name = c.name ORDER BY age_diff DESC;
