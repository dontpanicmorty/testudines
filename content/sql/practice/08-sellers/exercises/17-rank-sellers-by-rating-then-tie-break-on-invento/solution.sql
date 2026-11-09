WITH seller_totals AS (
  SELECT s.name, s.rating, COALESCE(SUM(i.price), 0) AS total_value
  FROM sellers s LEFT JOIN items i ON i.sellerId = s.id
  GROUP BY s.name, s.rating
)
SELECT name, rating, total_value FROM seller_totals ORDER BY rating DESC, total_value DESC;
