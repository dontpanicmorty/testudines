SELECT account_id, event_type, event_date, loaded_at FROM raw_usage_events QUALIFY ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY event_date DESC, loaded_at DESC) = 1 ORDER BY account_id;
