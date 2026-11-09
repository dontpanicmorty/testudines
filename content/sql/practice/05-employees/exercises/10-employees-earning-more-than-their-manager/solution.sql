SELECT e.name, e.salary FROM employees e JOIN employees m ON e.managerId = m.id WHERE e.salary > m.salary ORDER BY e.name;
