SELECT s.name FROM sellers s JOIN items i ON i.sellerId = s.id GROUP BY s.name HAVING COUNT(*) > 2 ORDER BY s.name;
