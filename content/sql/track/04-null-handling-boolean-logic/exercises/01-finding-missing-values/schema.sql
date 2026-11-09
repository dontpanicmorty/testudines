CREATE OR REPLACE TABLE accounts (account_id INTEGER, plan_name VARCHAR, cancelled_at DATE);
INSERT INTO accounts VALUES
  (1, 'starter', NULL),
  (2, 'pro', '2025-02-01'),
  (3, 'starter', NULL),
  (4, 'enterprise', NULL),
  (5, 'pro', '2025-05-15');
