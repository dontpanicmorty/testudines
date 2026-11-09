A model configured with `unique_key='event_id'` and `incremental_strategy='merge'`: when an incoming `event_id` already exists in the target, the incoming row replaces it.

Simulate the merge result: combine `existing_target` and `raw_usage_events`, then keep just one row per `event_id` -- the version with the greatest `loaded_at`.

Return `event_id`, `account_id`, `event_type`, `event_date`, `loaded_at`, ordered by `event_id`.
