Data quality issues mean a single account can match more than one territory_plan row (check the sample data -- Acme Corp matches two rows). Join `accounts` to `territory_plan` on `territory`, and keep only the highest-priority (lowest priority number) territory row per account.

Return `account_name`, `territory`, `plan_id`, `priority`, ordered by `account_name`.
