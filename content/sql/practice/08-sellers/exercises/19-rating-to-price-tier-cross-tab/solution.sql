WITH tiered AS (
  SELECT s.name AS seller_name,
         CASE WHEN i.price < 30 THEN 'budget' WHEN i.price <= 100 THEN 'mid' ELSE 'premium' END AS tier
  FROM sellers s JOIN items i ON i.sellerId = s.id
)
SELECT seller_name,
       SUM(CASE WHEN tier = 'budget' THEN 1 ELSE 0 END) AS budget_count,
       SUM(CASE WHEN tier = 'mid' THEN 1 ELSE 0 END) AS mid_count,
       SUM(CASE WHEN tier = 'premium' THEN 1 ELSE 0 END) AS premium_count
FROM tiered
GROUP BY seller_name
ORDER BY seller_name;
