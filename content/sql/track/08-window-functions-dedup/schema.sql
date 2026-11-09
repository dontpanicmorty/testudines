CREATE OR REPLACE TABLE events (
    event_id INTEGER, user_id INTEGER, event_type VARCHAR, event_ts TIMESTAMP, session_id VARCHAR
);
INSERT INTO events VALUES
 (1,1,'login','2024-01-01 08:00:00','s1'),
 (2,1,'view_page','2024-01-01 08:05:00','s1'),
 (3,1,'login','2024-01-02 09:00:00','s2'),
 (4,2,'login','2024-01-01 10:00:00','s3'),
 (5,2,'purchase','2024-01-01 10:15:00','s3'),
 (6,2,'login','2024-01-03 11:00:00','s4'),
 (7,3,'login','2024-01-01 12:00:00','s5');

CREATE OR REPLACE TABLE subscription_history (
    sub_id INTEGER, account_id INTEGER, status VARCHAR, effective_date DATE
);
INSERT INTO subscription_history VALUES
 (1,1,'trial','2023-01-01'),
 (1,1,'active','2023-02-01'),
 (1,1,'active','2023-03-01'),
 (1,1,'churned','2023-04-01'),
 (2,2,'active','2023-01-01');
