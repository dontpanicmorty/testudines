CREATE OR REPLACE TABLE shipments (shipment_id INTEGER, warehouse_code VARCHAR, order_id INTEGER, shipped_at DATE);
INSERT INTO shipments VALUES
  (1, 'WH1', 100, '2024-06-01'),
  (2, 'WH1', 101, '2025-06-01'),
  (3, 'WH2', 102, '2025-01-15');
CREATE OR REPLACE TABLE warehouse_rates (warehouse_code VARCHAR, effective_year INTEGER, rate_per_unit DECIMAL(10,2));
INSERT INTO warehouse_rates VALUES
  ('WH1', 2024, 1.50),
  ('WH1', 2025, 1.75),
  ('WH2', 2025, 2.00);
