SELECT account_id, account_name, created_at, created_at + INTERVAL 90 DAY AS stale_after FROM accounts ORDER BY account_id;
