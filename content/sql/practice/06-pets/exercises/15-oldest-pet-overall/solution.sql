SELECT name, pet_type, age FROM (SELECT name, age, 'dog' AS pet_type FROM dogs UNION ALL SELECT name, age, 'cat' FROM cats) t ORDER BY age DESC LIMIT 1;
