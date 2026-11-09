SELECT employeeId, id, amount, MAX(amount) OVER (PARTITION BY employeeId) AS employee_max_sale FROM sales ORDER BY employeeId, amount DESC;
