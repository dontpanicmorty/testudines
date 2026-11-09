CREATE OR REPLACE TABLE orders (order_id INTEGER, order_date DATE, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, '2025-01-05', 50.00),
  (2, '2025-01-20', 30.00),
  (3, '2025-02-02', 45.00),
  (4, '2025-02-25', 15.00),
  (5, '2025-03-10', 60.00);
