SELECT e.name AS employee_name, gm.name AS skip_level_manager FROM employees e JOIN employees m ON e.managerId = m.id JOIN employees gm ON m.managerId = gm.id ORDER BY e.name;
