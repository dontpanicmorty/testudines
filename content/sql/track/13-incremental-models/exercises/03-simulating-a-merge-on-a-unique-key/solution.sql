WITH combined AS (
  SELECT * FROM existing_target
  UNION ALL
  SELECT * FROM raw_usage_events
)
SELECT event_id, account_id, event_type, event_date, loaded_at
FROM combined
QUALIFY ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY loaded_at DESC) = 1
ORDER BY event_id;
