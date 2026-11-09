SELECT id, account_id, len(CAST(payload::JSON->'features' AS VARCHAR[])) AS feature_count FROM raw_payloads ORDER BY id;
