select
    subscription_id
  , plan_name
  , status
from subscriptions
where (status = 'active' and not is_trial)
   or plan_name = 'enterprise'
order by subscription_id
