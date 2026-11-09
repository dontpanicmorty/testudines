WITH emp_totals AS (
  SELECT e.id, e.name, st.regionId, COALESCE(SUM(s.amount), 0) AS total_sales
  FROM employees e JOIN states st ON e.stateId = st.id LEFT JOIN sales s ON s.employeeId = e.id
  GROUP BY e.id, e.name, st.regionId
)
SELECT name FROM emp_totals
WHERE total_sales > (
  SELECT AVG(total_sales) FROM emp_totals et2 JOIN regions r ON et2.regionId = r.id WHERE r.name = 'South'
)
ORDER BY name;
