dbt's `not_null` generic test works by finding rows where the column IS NULL -- if any come back, the test fails.

Write the query dbt would effectively run to test that `owner_id` is not_null on `accounts` -- return all columns for the rows that would fail this test.
