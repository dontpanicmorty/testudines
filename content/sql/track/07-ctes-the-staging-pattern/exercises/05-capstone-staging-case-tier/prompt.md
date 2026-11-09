Write a query with `subs` and `accounts` CTEs that returns, for every subscription (trial or not): `account_name`, `plan_code`, `mrr`, and a computed `plan_tier` column ('trial' when is_trial, else 'paid').

Order by `account_name`, then `plan_code`.
