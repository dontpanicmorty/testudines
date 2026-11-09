Build a miniature dbt.

`run_models(con, models)` takes an open DuckDB connection and a dict `{model_name: sql_template}`. Templates may contain `{{ ref('other_model') }}`. Build every model as a table named after it, **parents before children**, using `CREATE OR REPLACE TABLE name AS <sql>`. Return the list of model names in the order they were built.

- A ref to a model that is not in `models` raises `KeyError`.
- A dependency cycle raises `ValueError`.
- Running it twice must leave the same tables (idempotent).
- Models with no relationship may be built in any order.

```python
models = {
    "totals": "SELECT cust, SUM(amt) AS total FROM {{ ref('orders') }} GROUP BY cust",
    "orders": "SELECT * FROM (VALUES ('a', 1), ('a', 2)) t(cust, amt)",
}
run_models(con, models)    # ["orders", "totals"]
```
