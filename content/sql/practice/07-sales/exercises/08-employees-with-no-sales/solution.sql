SELECT e.name FROM employees e LEFT JOIN sales s ON s.employeeId = e.id WHERE s.id IS NULL ORDER BY e.name;
