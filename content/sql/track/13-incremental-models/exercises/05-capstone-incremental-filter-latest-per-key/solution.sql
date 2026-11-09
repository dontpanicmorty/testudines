WITH new_rows AS (
  SELECT * FROM raw_usage_events WHERE loaded_at > (SELECT MAX(loaded_at) FROM existing_target)
)
SELECT account_id, event_type, event_date, loaded_at
FROM new_rows
QUALIFY ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY event_date DESC, loaded_at DESC) = 1
ORDER BY account_id;
