SELECT e.name, SUM(s.amount) AS total_sales FROM employees e JOIN sales s ON s.employeeId = e.id GROUP BY e.name ORDER BY total_sales DESC;
