CREATE OR REPLACE TABLE price_history (product_id INTEGER, effective_date DATE, price DECIMAL(10,2));
INSERT INTO price_history VALUES
  (1, '2025-01-01', 9.99),
  (1, '2025-01-01', 10.99),
  (1, '2025-02-01', 11.99),
  (2, '2025-01-01', 19.99),
  (2, '2025-01-01', 19.99);
