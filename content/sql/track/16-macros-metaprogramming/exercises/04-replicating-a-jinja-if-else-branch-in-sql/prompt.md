A macro's Jinja loop often does: {% if column.dtype == 'TIMESTAMP_TZ' %}{{ column }}::timestamp_ntz{% else %}{{ column }}{% endif %}.

For each row in `columns_metadata`, return `column_name` and a computed `cast_expression` string: if data_type = 'TIMESTAMP_TZ', return '<column_name>::timestamp_ntz'; otherwise just '<column_name>'.

Order by `column_name`.
