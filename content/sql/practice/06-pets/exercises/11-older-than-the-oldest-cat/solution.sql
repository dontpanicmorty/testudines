SELECT name, age FROM dogs WHERE age > (SELECT MAX(age) FROM cats);
