WITH seller_totals AS (
  SELECT s.name, SUM(i.price) AS total_value FROM sellers s JOIN items i ON i.sellerId = s.id GROUP BY s.name
)
SELECT name, total_value, ROUND(100.0 * total_value / SUM(total_value) OVER (), 1) AS pct_of_catalog
FROM seller_totals
ORDER BY pct_of_catalog DESC;
