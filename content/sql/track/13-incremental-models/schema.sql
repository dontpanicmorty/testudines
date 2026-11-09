CREATE OR REPLACE TABLE existing_target (
    event_id INTEGER, account_id INTEGER, event_type VARCHAR, event_date DATE, loaded_at TIMESTAMP
);
INSERT INTO existing_target VALUES
 (1,1,'login','2024-01-01','2024-01-01 00:05:00'),
 (2,2,'login','2024-01-01','2024-01-01 00:06:00');

CREATE OR REPLACE TABLE raw_usage_events (
    event_id INTEGER, account_id INTEGER, event_type VARCHAR, event_date DATE, loaded_at TIMESTAMP
);
INSERT INTO raw_usage_events VALUES
 (1,1,'login_updated','2024-01-01','2024-01-05 00:00:00'),
 (2,2,'login','2024-01-01','2024-01-01 00:06:00'),
 (3,1,'purchase','2024-01-10','2024-01-10 00:00:00'),
 (4,3,'login','2024-01-11','2024-01-11 00:00:00'),
 (5,3,'purchase','2024-01-12','2024-01-12 00:00:00');
