SELECT id, account_id, payload::JSON->>'plan' AS plan FROM raw_payloads ORDER BY id;
