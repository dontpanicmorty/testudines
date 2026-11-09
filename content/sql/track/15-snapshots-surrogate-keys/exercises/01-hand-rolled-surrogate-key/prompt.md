This repo generates surrogate keys via {{ dbt_utils.generate_surrogate_key([...]) }}, which under the hood MD5-hashes the concatenated, null-safe-coalesced columns.

Using md5(), write a query returning `employee_id`, `department`, and a `surrogate_key` column computed as:
md5(coalesce(employee_id::varchar,'') || '-' || coalesce(department,''))
against `daily_feed_day1`.

Order by `employee_id`.
