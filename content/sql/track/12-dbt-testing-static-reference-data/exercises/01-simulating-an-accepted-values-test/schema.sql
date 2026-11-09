CREATE OR REPLACE TABLE subscriptions (subscription_id INTEGER, status VARCHAR);
INSERT INTO subscriptions VALUES
  (1, 'active'),
  (2, 'trialing'),
  (3, 'pending'),
  (4, 'cancelled'),
  (5, 'archived');
