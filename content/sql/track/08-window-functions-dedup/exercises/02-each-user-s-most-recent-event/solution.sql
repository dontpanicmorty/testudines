SELECT user_id, event_type, event_ts FROM events QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts DESC) = 1 ORDER BY user_id;
