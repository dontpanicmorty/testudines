CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 1, 10.00),
  (2, 2, 50.00),
  (3, 3, 20.00),
  (4, 1, 90.00),
  (5, 2, 30.00);
