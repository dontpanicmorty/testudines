CREATE OR REPLACE TABLE support_tickets (ticket_id INTEGER, description VARCHAR);
INSERT INTO support_tickets VALUES
  (1, '{{customer}} cannot log in'),
  (2, 'Billing question from {{customer}}'),
  (3, '{{customer}} requests refund'),
  (4, 'App crash reported by {{customer}}');
