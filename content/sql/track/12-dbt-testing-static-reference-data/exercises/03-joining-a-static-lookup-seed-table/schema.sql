CREATE OR REPLACE TABLE orders (order_id INTEGER, status_code VARCHAR, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 'A', 10.00),
  (2, 'B', 20.00),
  (3, 'A', 15.00),
  (4, 'C', 5.00);
CREATE OR REPLACE TABLE status_lookup (status_code VARCHAR, status_label VARCHAR);
INSERT INTO status_lookup VALUES
  ('A', 'Open'),
  ('B', 'Shipped'),
  ('C', 'Cancelled');
