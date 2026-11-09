SELECT employeeId, COUNT(*) AS sale_count FROM sales GROUP BY employeeId ORDER BY employeeId;
