CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, amount DECIMAL(10,2), status VARCHAR);
INSERT INTO orders VALUES
  (1, 100, 25.50, 'shipped'),
  (2, 101, 10.00, 'pending'),
  (3, 102, 40.25, 'shipped');
