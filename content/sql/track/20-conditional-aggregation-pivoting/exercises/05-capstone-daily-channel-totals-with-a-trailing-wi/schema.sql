CREATE OR REPLACE TABLE daily_sales (sale_date DATE, channel VARCHAR, amount DECIMAL(10,2));
INSERT INTO daily_sales VALUES
  ('2025-01-01', 'online', 10.00),
  ('2025-01-01', 'retail', 5.00),
  ('2025-01-02', 'online', 20.00),
  ('2025-01-02', 'retail', 8.00),
  ('2025-01-03', 'online', 30.00),
  ('2025-01-03', 'retail', 12.00),
  ('2025-01-04', 'online', 5.00),
  ('2025-01-04', 'retail', 3.00);
