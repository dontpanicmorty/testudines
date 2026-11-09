SELECT id, employeeId, amount FROM sales s WHERE amount > (SELECT AVG(amount) FROM sales s2 WHERE s2.employeeId = s.employeeId) ORDER BY employeeId, amount DESC;
