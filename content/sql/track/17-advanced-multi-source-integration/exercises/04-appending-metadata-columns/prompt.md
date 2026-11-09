Models here habitually append metadata columns at the end of the final select (table_owner, load_date).

Take the join logic from 17.3 and add two literal columns: `table_owner` = 'analytics_eng' and `load_date` = DATE '2024-06-01' (standing in for CURRENT_DATE in this exercise).

Return `account_name`, `territory`, `contract_value`, `table_owner`, `load_date`, ordered by `account_name`.
