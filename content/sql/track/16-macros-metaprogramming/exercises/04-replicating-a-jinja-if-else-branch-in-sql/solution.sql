SELECT column_name, CASE WHEN data_type = 'TIMESTAMP_TZ' THEN column_name || '::timestamp_ntz' ELSE column_name END AS cast_expression FROM columns_metadata ORDER BY column_name;
