For every team across all accounts (flatten teams as in 14.2), return `account_id`, the account's `plan` (top-level field), `team_id`, `seats`, and a computed `team_size_tier` column ('large' when seats >= 5, else 'small').

Order by `account_id`, then `team_id`.
