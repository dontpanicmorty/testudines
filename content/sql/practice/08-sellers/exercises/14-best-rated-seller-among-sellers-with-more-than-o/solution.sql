WITH multi_item_sellers AS (
  SELECT s.id, s.name, s.rating FROM sellers s JOIN items i ON i.sellerId = s.id GROUP BY s.id, s.name, s.rating HAVING COUNT(*) > 1
)
SELECT name, rating FROM multi_item_sellers ORDER BY rating DESC LIMIT 1;
