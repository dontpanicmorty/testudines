WITH stg_subscriptions AS (
  SELECT * FROM source_subscriptions WHERE is_trial = false
),
stg_accounts AS (
  SELECT * FROM source_accounts
),
joined AS (
  SELECT s.plan_code, s.mrr, a.account_name
  FROM stg_subscriptions s
  LEFT JOIN stg_accounts a ON s.account_id = a.account_id
)
SELECT COALESCE(account_name, 'Unknown') AS account_name, plan_code, mrr
FROM joined
ORDER BY plan_code, account_name;
