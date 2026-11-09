dbt's `dbt_utils.unique_combination_of_columns` test would check that `(product_id, effective_date)` is unique in `price_history`. Simulate that: return the `product_id`, `effective_date`, and `row_count` for any combination appearing more than once -- these are the rows that would fail the test.

Order by `product_id`, `effective_date`.
