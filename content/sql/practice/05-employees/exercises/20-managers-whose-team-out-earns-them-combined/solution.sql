SELECT m.name FROM employees m WHERE (SELECT SUM(e.salary) FROM employees e WHERE e.managerId = m.id) > m.salary ORDER BY m.name;
