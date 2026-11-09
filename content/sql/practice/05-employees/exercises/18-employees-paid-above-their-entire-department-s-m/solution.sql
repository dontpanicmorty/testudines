SELECT e.name, e.department, e.salary FROM employees e WHERE e.salary > (SELECT MEDIAN(e2.salary) FROM employees e2 WHERE e2.department = e.department) ORDER BY e.department, e.salary DESC;
