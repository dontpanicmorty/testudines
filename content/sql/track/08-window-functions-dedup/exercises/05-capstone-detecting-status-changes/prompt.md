Return `sub_id`, `effective_date`, `status`, and a boolean column `status_changed` indicating whether status differs from the previous row's status for that `sub_id`. The first row for a `sub_id` should always show `status_changed = true`.

Order by `sub_id`, then `effective_date`.
