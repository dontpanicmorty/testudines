CREATE OR REPLACE TABLE daily_sales (sale_date DATE, region VARCHAR, amount DECIMAL(10,2));
INSERT INTO daily_sales VALUES
  ('2025-01-01', 'west', 10.00),
  ('2025-01-02', 'west', 20.00),
  ('2025-01-03', 'west', 30.00),
  ('2025-01-04', 'west', 5.00),
  ('2025-01-01', 'east', 100.00),
  ('2025-01-02', 'east', 50.00);
