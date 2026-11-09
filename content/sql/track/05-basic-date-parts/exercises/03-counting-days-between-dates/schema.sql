CREATE OR REPLACE TABLE subscriptions (subscription_id INTEGER, started_at DATE, cancelled_at DATE);
INSERT INTO subscriptions VALUES
  (1, '2025-01-01', '2025-01-11'),
  (2, '2025-02-01', '2025-02-05'),
  (3, '2025-03-01', '2025-03-31'),
  (4, '2025-04-10', '2025-04-12');
