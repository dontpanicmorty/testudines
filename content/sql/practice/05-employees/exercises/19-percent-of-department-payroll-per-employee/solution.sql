SELECT name, department, salary, ROUND(100.0 * salary / SUM(salary) OVER (PARTITION BY department), 1) AS pct_of_dept_payroll FROM employees ORDER BY department, pct_of_dept_payroll DESC;
