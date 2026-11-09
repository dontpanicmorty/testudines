There's a small `legacy_subscriptions` table left over from a previous system, with the same account_id/plan_code shape.

Return `account_id`, `plan_code`, and a literal column `source_system` set to 'current' for rows from `source_subscriptions`, combined with rows from `legacy_subscriptions` tagged 'legacy', so every row from both tables appears in the result.

Order by `account_id`, then `source_system`.
