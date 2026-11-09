select
    account_id
  , plan_name
from accounts
where cancelled_at is null
order by account_id
