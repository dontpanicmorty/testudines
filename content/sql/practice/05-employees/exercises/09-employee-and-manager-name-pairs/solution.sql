SELECT e.name AS employee_name, m.name AS manager_name FROM employees e JOIN employees m ON e.managerId = m.id ORDER BY e.name;
