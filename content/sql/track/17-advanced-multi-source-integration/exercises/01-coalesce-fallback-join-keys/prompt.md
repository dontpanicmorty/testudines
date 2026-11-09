Two systems can identify the same account by either `accountid_a` or `accountid_b` -- never both reliably populated on both sides. This repo's models constantly bridge that gap with a fallback-key join pattern.

Join `territory_plan` to `accounts_multi` using that fallback-key approach, matching on whichever id is populated on each side. Return `account_name`, `territory`, `plan_id`.

Order by `plan_id`.
