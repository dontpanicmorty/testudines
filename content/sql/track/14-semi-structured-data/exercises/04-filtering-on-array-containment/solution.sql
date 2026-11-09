SELECT id, account_id FROM raw_payloads WHERE list_contains(CAST(payload::JSON->'features' AS VARCHAR[]), 'sso') ORDER BY id;
