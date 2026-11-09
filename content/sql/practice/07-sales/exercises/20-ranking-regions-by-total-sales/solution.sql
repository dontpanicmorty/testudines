WITH region_totals AS (
  SELECT r.name, COALESCE(SUM(s.amount), 0) AS total_sales
  FROM regions r
  LEFT JOIN states st ON st.regionId = r.id
  LEFT JOIN employees e ON e.stateId = st.id
  LEFT JOIN sales s ON s.employeeId = e.id
  GROUP BY r.name
)
SELECT name, total_sales, DENSE_RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM region_totals
ORDER BY sales_rank;
