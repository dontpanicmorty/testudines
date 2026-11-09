SELECT name, department, salary, ROUND(salary - AVG(salary) OVER (PARTITION BY department), 0) AS diff_from_avg FROM employees ORDER BY department, name;
