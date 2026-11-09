WITH acct AS (SELECT * FROM accounts_multi),
territory AS (
  SELECT a.account_key, t.territory
  FROM territory_plan t
  JOIN accounts_multi a ON COALESCE(t.accountid_a, t.accountid_b) = COALESCE(a.accountid_a, a.accountid_b)
  QUALIFY DENSE_RANK() OVER (PARTITION BY a.account_key ORDER BY t.priority) = 1
),
contracts AS (SELECT * FROM web_contracts)
SELECT acct.account_name,
       territory.territory,
       COALESCE(contracts.contract_value, 0) AS contract_value
FROM acct
LEFT JOIN territory ON territory.account_key = acct.account_key
LEFT JOIN contracts ON contracts.accountid_a = acct.accountid_a
ORDER BY acct.account_name;
