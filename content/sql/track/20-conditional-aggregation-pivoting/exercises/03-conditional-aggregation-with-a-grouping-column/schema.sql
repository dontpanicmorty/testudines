CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, channel VARCHAR, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 1, 'online', 10.00),
  (2, 1, 'retail', 20.00),
  (3, 2, 'online', 15.00),
  (4, 2, 'online', 5.00),
  (5, 3, 'retail', 30.00);
