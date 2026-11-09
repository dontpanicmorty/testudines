Build a query with three CTEs: `acct` (accounts_multi), `territory` (the deduped territory_plan logic from 17.2, projecting account_key and territory), and `contracts` (web_contracts, keyed only by accountid_a).

Combine all three so every account appears even without a territory or contract match. Return `account_name`, `territory` (NULL if none), and `contract_value` (0 if none).

Order by `account_name`.
