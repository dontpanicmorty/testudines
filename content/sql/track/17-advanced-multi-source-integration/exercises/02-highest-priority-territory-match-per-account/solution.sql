SELECT a.account_name, t.territory, t.plan_id, t.priority
FROM territory_plan t
JOIN accounts_multi a ON COALESCE(t.accountid_a, t.accountid_b) = COALESCE(a.accountid_a, a.accountid_b)
QUALIFY DENSE_RANK() OVER (PARTITION BY COALESCE(a.accountid_a, a.accountid_b) ORDER BY t.priority) = 1
ORDER BY a.account_name;
