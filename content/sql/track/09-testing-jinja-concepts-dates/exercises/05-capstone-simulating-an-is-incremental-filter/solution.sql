SELECT account_id, account_name, created_at FROM accounts WHERE created_at >= DATE '2024-04-01' - INTERVAL 60 DAY ORDER BY created_at;
