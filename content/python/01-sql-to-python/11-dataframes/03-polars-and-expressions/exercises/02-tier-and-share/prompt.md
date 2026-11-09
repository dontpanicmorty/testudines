Write `add_tier_and_share(df)` returning `df` with two extra columns, keeping row order:

- `tier`: `"large"` if `amount >= 100`, `"medium"` if `amount >= 50`, otherwise `"small"`.
- `region_share`: the row's `amount` divided by the total `amount` of its region, rounded to 3 decimals.

Input has `order_id`, `region`, `amount`.
