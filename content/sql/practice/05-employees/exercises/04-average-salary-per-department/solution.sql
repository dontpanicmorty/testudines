SELECT department, ROUND(AVG(salary), 0) AS avg_salary FROM employees GROUP BY department ORDER BY department;
