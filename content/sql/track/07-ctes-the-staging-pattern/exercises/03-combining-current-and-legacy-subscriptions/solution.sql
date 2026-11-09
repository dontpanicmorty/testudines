SELECT account_id, plan_code, 'current' AS source_system FROM source_subscriptions
UNION ALL
SELECT account_id, plan_code, 'legacy' AS source_system FROM legacy_subscriptions
ORDER BY account_id, source_system;
