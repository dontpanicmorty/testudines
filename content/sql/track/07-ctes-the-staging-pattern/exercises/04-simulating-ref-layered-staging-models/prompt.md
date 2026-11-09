Models here almost never query raw sources directly -- they build through ref()'d staging models. Simulate that layering:

Build a `stg_subscriptions` CTE (non-trial subscriptions only) and a `stg_accounts` CTE, then a final `joined` CTE that connects stg_subscriptions to stg_accounts, keeping every subscription even if its account record is missing.

From `joined`, select `account_name` (defaulted to 'Unknown' if the account record is missing), `plan_code`, and `mrr`.

Order by `plan_code`, then `account_name`.

(One subscription in the sample data references an account_id that doesn't exist in source_accounts -- that's the row your default needs to catch.)
