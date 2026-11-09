SELECT s.name, SUM(i.price) AS total_value FROM sellers s JOIN items i ON i.sellerId = s.id GROUP BY s.name ORDER BY total_value DESC;
