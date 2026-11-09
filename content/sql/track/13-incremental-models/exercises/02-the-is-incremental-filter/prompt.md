On subsequent incremental runs, dbt's `{% if is_incremental() %}` block typically adds a filter so only new rows get processed.

`existing_target` represents what's already in the warehouse. Write that filtered query against `raw_usage_events`: only rows that are newer than what's already been loaded into `existing_target`.

Return the same columns as 13.1, ordered by `event_id`.
