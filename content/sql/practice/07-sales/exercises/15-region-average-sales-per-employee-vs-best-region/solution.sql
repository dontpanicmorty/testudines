WITH employee_regions AS (
  SELECT e.id AS employeeid, st.regionId AS regionid FROM employees e JOIN states st ON e.stateId = st.id
),
regional_sales AS (
  SELECT er.regionid, COUNT(DISTINCT er.employeeid) AS emp_count, COALESCE(SUM(s.amount), 0) AS total_sales
  FROM employee_regions er LEFT JOIN sales s ON er.employeeid = s.employeeId
  GROUP BY er.regionid
),
regional_avg AS (
  SELECT r.name, CASE WHEN rs.emp_count IS NULL OR rs.emp_count = 0 THEN 0 ELSE rs.total_sales / rs.emp_count END AS avg_sales
  FROM regions r LEFT JOIN regional_sales rs ON r.id = rs.regionid
)
SELECT name, avg_sales, (SELECT MAX(avg_sales) FROM regional_avg) - avg_sales AS avg_sales_delta
FROM regional_avg
ORDER BY avg_sales DESC, name;
