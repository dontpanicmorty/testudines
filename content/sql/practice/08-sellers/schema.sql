CREATE OR REPLACE TABLE sellers (id INTEGER, name VARCHAR, rating INTEGER);
INSERT INTO sellers VALUES (1,'Acme Goods',5),(2,'Bright Bazaar',3),(3,'Cedar Mart',4),(4,'Dune Traders',2);

CREATE OR REPLACE TABLE items (id INTEGER, name VARCHAR, sellerId INTEGER, price DECIMAL(8,2));
INSERT INTO items VALUES
 (1,'Lamp',1,25.00),(2,'Chair',1,60.00),(3,'Desk',2,150.00),(4,'Mug',3,8.00),
 (5,'Rug',3,120.00),(6,'Vase',4,15.00),(7,'Shelf',2,45.00),(8,'Pillow',1,20.00);
