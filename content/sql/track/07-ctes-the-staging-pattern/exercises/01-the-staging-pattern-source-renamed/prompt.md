Almost every staging model in this repo follows a `source` CTE -> `renamed` CTE -> final select pattern.

Write a query with a `source` CTE selecting from `source_subscriptions`, and a `renamed` CTE that renames `sub_id` -> `subscription_id` and `mrr` -> `monthly_recurring_revenue` (keep `account_id` and `plan_code` as-is).

Select all columns from `renamed`, ordered by `subscription_id`.
