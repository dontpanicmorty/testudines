CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, order_date DATE, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 1, '2025-01-01', 10.00),
  (2, 1, '2025-02-01', 20.00),
  (3, 1, '2025-03-01', 30.00),
  (4, 2, '2025-01-15', 5.00),
  (5, 2, '2025-02-15', 15.00);
