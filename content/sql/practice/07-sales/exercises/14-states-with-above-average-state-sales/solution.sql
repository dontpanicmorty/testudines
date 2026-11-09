WITH state_totals AS (
  SELECT st.name, COALESCE(SUM(sa.amount), 0) AS total_sales
  FROM states st LEFT JOIN employees e ON e.stateId = st.id LEFT JOIN sales sa ON sa.employeeId = e.id
  GROUP BY st.name
)
SELECT name, total_sales FROM state_totals
WHERE total_sales > (SELECT AVG(total_sales) FROM state_totals)
ORDER BY total_sales DESC;
