SELECT name, age, pet_type, RANK() OVER (ORDER BY age DESC) AS age_rank FROM (SELECT name, age, 'dog' AS pet_type FROM dogs UNION ALL SELECT name, age, 'cat' FROM cats) t ORDER BY age_rank;
