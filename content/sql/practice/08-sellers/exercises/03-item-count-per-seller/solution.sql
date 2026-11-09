SELECT sellerId, COUNT(*) AS item_count FROM items GROUP BY sellerId ORDER BY sellerId;
