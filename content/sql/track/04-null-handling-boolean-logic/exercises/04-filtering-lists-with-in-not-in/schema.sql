CREATE OR REPLACE TABLE events (event_id INTEGER, event_type VARCHAR);
INSERT INTO events VALUES
  (1, 'signup'),
  (2, 'login'),
  (3, 'upgrade'),
  (4, 'logout'),
  (5, 'renewal'),
  (6, 'cancellation');
