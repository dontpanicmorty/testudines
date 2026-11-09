Combine both concepts: from `raw_usage_events`, keep only rows newer than existing_target's max loaded_at (the incremental filter from 13.2), and within that filtered set return just the latest event per account_id (as in 13.4).

Return `account_id`, `event_type`, `event_date`, `loaded_at`, ordered by `account_id`.
