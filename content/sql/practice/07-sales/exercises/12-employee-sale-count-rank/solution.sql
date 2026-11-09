SELECT e.name, COUNT(s.id) AS sale_count, RANK() OVER (ORDER BY COUNT(s.id) DESC) AS sale_rank FROM employees e LEFT JOIN sales s ON s.employeeId = e.id GROUP BY e.name ORDER BY sale_rank;
