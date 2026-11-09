Macros that generate SQL dynamically usually start by introspecting a relation's columns (like adapter.get_columns_in_relation). `columns_metadata` simulates that introspection result.

Return, for each `data_type` present, the count of columns with that type (alias `column_count`).

Order by `data_type`.
