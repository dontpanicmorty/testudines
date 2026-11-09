Build a query with two CTEs: `subs` (subscriptions where is_trial = false) and `accounts` (all of source_accounts). Join them in the final select to return `account_name`, `plan_code`, and `mrr` for every non-trial subscription.

Order by `account_name`, then `plan_code`.
