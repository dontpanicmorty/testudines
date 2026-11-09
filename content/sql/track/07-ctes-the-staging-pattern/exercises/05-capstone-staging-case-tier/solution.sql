WITH subs AS (
  SELECT * FROM source_subscriptions
),
accounts AS (
  SELECT * FROM source_accounts
)
SELECT a.account_name, s.plan_code, s.mrr,
       CASE WHEN s.is_trial THEN 'trial' ELSE 'paid' END AS plan_tier
FROM subs s
JOIN accounts a ON s.account_id = a.account_id
ORDER BY a.account_name, s.plan_code;
