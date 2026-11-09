WITH region_totals AS (
  SELECT r.name, COALESCE(SUM(s.amount), 0) AS total_sales
  FROM regions r
  LEFT JOIN states st ON st.regionId = r.id
  LEFT JOIN employees e ON e.stateId = st.id
  LEFT JOIN sales s ON s.employeeId = e.id
  GROUP BY r.name
)
SELECT name, total_sales, ROUND(100.0 * total_sales / SUM(total_sales) OVER (), 1) AS pct_of_company
FROM region_totals
ORDER BY pct_of_company DESC;
