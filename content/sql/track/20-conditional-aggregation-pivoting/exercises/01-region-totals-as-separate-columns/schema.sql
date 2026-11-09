CREATE OR REPLACE TABLE orders (order_id INTEGER, region VARCHAR, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 'west', 10.00),
  (2, 'east', 20.00),
  (3, 'west', 15.00),
  (4, 'north', 5.00),
  (5, 'east', 25.00);
