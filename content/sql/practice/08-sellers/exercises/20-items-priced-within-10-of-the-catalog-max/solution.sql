SELECT i.name AS item_name, s.name AS seller_name, i.price FROM items i JOIN sellers s ON i.sellerId = s.id WHERE i.price >= 0.9 * (SELECT MAX(price) FROM items) ORDER BY i.price DESC;
