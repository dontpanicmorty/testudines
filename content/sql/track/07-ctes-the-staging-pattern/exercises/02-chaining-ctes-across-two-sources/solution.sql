WITH subs AS (
  SELECT * FROM source_subscriptions WHERE is_trial = false
),
accounts AS (
  SELECT * FROM source_accounts
)
SELECT a.account_name, s.plan_code, s.mrr
FROM subs s
JOIN accounts a ON s.account_id = a.account_id
ORDER BY a.account_name, s.plan_code;
