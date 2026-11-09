SELECT s.name AS seller_name, i.name AS item_name, i.price FROM sellers s JOIN items i ON i.sellerId = s.id QUALIFY ROW_NUMBER() OVER (PARTITION BY s.id ORDER BY i.price DESC) = 2 ORDER BY s.name;
