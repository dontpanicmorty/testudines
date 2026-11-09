CREATE OR REPLACE TABLE subscriptions (subscription_id INTEGER, plan_name VARCHAR, status VARCHAR, is_trial BOOLEAN);
INSERT INTO subscriptions VALUES
  (1, 'starter', 'active', false),
  (2, 'starter', 'active', true),
  (3, 'enterprise', 'active', true),
  (4, 'pro', 'cancelled', false),
  (5, 'enterprise', 'cancelled', false);
