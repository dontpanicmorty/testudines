delete+insert incremental models often keep just the latest known state per key. Return only the most recent event per `account_id` from `raw_usage_events` (the row with the latest `event_date`, tie-broken by the latest `loaded_at`).

Return `account_id`, `event_type`, `event_date`, `loaded_at`, ordered by `account_id`.
