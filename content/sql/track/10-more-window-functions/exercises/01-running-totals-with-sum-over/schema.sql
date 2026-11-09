CREATE OR REPLACE TABLE payments (payment_id INTEGER, account_id INTEGER, paid_at DATE, amount DECIMAL(10,2));
INSERT INTO payments VALUES
  (1, 1, '2025-01-01', 10.00),
  (2, 1, '2025-02-01', 20.00),
  (3, 1, '2025-03-01', 15.00),
  (4, 2, '2025-01-10', 5.00),
  (5, 2, '2025-02-10', 25.00);
