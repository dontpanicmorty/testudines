WITH totals AS (
  SELECT r.name AS region_name, e.name AS employee_name, SUM(s.amount) AS total_sales
  FROM regions r JOIN states st ON st.regionId = r.id JOIN employees e ON e.stateId = st.id JOIN sales s ON s.employeeId = e.id
  GROUP BY r.name, e.name
)
SELECT region_name, employee_name, total_sales FROM totals
QUALIFY ROW_NUMBER() OVER (PARTITION BY region_name ORDER BY total_sales DESC) = 1
ORDER BY region_name;
