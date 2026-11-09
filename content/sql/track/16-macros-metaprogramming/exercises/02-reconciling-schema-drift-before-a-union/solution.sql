SELECT id, name, amount, created_at::VARCHAR AS created_at, 'a' AS source_system FROM source_a
UNION ALL
SELECT id, name, amount_usd::DECIMAL(10,2) AS amount, created_ts::VARCHAR AS created_at, 'b' AS source_system FROM source_b
ORDER BY id, source_system;
