SELECT event_id, account_id, event_type, event_date, loaded_at FROM raw_usage_events WHERE loaded_at > (SELECT MAX(loaded_at) FROM existing_target) ORDER BY event_id;
