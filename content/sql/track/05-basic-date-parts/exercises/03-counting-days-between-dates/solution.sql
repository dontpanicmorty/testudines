select
    subscription_id
  , cancelled_at - started_at as days_active
from subscriptions
order by subscription_id
