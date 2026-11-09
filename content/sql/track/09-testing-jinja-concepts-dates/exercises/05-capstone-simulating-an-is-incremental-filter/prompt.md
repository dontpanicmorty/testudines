dbt models often branch logic with {% if is_incremental() %}, usually to add a recency filter. Simulate that filter here.

Pretend "today" is DATE '2024-04-01' (don't use CURRENT_DATE for this exercise -- hardcode that literal). Return `account_id`, `account_name`, `created_at` for accounts created within the last 60 days of that date.

Order by `created_at`.
