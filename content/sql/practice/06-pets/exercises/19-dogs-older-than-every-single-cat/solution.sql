SELECT name, age FROM dogs WHERE age > ALL (SELECT age FROM cats) ORDER BY name;
