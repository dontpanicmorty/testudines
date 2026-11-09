SELECT user_id, event_type, event_ts, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts) AS event_seq FROM events ORDER BY user_id, event_seq;
