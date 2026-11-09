Bring it all together: for each account, return `account_name`, `territory` (top-priority), `contract_value` (defaulted to 0), a computed `account_tier` column ('key_account' when contract_value > 4000, else 'standard'), and the literal `table_owner` = 'analytics_eng'.

Order by `contract_value` descending.
