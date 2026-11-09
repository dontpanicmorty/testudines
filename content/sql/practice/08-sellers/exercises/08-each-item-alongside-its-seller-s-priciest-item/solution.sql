SELECT s.name AS seller_name, i.name AS item_name, i.price, MAX(i.price) OVER (PARTITION BY s.id) AS seller_max_price FROM sellers s JOIN items i ON i.sellerId = s.id ORDER BY s.name, i.price DESC;
