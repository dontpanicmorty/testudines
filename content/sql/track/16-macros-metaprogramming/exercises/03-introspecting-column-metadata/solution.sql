SELECT data_type, COUNT(*) AS column_count FROM columns_metadata GROUP BY data_type ORDER BY data_type;
