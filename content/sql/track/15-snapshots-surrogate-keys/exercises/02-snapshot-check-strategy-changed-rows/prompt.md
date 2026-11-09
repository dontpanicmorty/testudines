A dbt snapshot with `strategy='check'` detects when tracked columns change between runs.

Compare `daily_feed_day1` (yesterday) to `daily_feed_day2` (today) and return `employee_id`, `department`, `salary` from today's feed for every employee whose department or salary changed between the two days -- including a change from/to a missing (null) value.

Order by `employee_id`.
