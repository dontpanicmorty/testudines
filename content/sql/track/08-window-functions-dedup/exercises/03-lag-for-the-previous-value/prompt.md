`subscription_history` has one row per status change per `sub_id`. Return `sub_id`, `effective_date`, `status`, and the previous status for that `sub_id` (alias `previous_status`, NULL if none).

Order by `sub_id`, then `effective_date`.
