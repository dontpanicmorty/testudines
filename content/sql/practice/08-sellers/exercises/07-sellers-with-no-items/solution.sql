SELECT s.name FROM sellers s LEFT JOIN items i ON i.sellerId = s.id WHERE i.id IS NULL ORDER BY s.name;
