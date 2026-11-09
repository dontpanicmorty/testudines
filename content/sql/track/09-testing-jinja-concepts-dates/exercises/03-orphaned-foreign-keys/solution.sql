SELECT p.plan_id, p.account_id FROM plan_accounts p LEFT JOIN accounts a ON p.account_id = a.account_id WHERE a.account_id IS NULL ORDER BY p.plan_id;
