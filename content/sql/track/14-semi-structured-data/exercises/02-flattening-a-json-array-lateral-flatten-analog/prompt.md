Snowflake explodes a JSON array into one row per element with `LATERAL FLATTEN(input => payload:teams)`. DuckDB's equivalent involves casting the array to a typed list and using `UNNEST`.

Return `id`, `account_id`, `team_id`, and `seats` -- one row per team across all accounts. Accounts with no teams should be skipped automatically.

Order by `id`, then `team_id`.
