CREATE OR REPLACE TABLE leads (lead_id INTEGER, source VARCHAR, converted_at DATE, is_qualified BOOLEAN);
INSERT INTO leads VALUES
  (1, 'ads', '2025-01-05', true),
  (2, 'ads', NULL, true),
  (3, 'referral', NULL, NULL),
  (4, 'organic', '2025-02-10', false),
  (5, 'referral', '2025-03-01', false);
