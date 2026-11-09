select
    subscription_id
  , status
from subscriptions
where status not in ('active', 'trialing', 'cancelled', 'past_due')
order by subscription_id
