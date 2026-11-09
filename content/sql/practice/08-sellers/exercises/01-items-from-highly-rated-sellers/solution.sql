SELECT i.name AS item_name, s.name AS seller_name FROM items i JOIN sellers s ON i.sellerId = s.id WHERE s.rating > 4 ORDER BY i.name;
