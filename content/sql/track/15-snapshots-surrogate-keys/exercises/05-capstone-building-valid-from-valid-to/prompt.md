`employee_history` has one row per (employee_id, change), each with a valid_from date -- this is what a chain of snapshot runs accumulates over time.

Compute `valid_to` for each row as the next change's `valid_from` for that `employee_id` (leave it NULL for the most recent, still-open row).

Return `employee_id`, `department`, `salary`, `valid_from`, `valid_to`, ordered by `employee_id`, then `valid_from`.
