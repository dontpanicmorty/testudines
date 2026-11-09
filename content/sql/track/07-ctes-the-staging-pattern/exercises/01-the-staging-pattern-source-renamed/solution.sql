WITH source AS (
    SELECT * FROM source_subscriptions
),
renamed AS (
    SELECT
        sub_id AS subscription_id
        , account_id
        , plan_code
        , mrr AS monthly_recurring_revenue
    FROM source
)
SELECT * FROM renamed ORDER BY subscription_id;
