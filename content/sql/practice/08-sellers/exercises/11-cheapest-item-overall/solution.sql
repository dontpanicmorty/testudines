SELECT i.name AS item_name, s.name AS seller_name, i.price FROM items i JOIN sellers s ON i.sellerId = s.id ORDER BY i.price ASC LIMIT 1;
