SELECT a.account_name, t.territory, t.plan_id FROM territory_plan t JOIN accounts_multi a ON COALESCE(t.accountid_a, t.accountid_b) = COALESCE(a.accountid_a, a.accountid_b) ORDER BY t.plan_id;
