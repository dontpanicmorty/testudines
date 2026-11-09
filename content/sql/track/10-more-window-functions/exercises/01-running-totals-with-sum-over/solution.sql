select
    payment_id
  , account_id
  , paid_at
  , amount
  , sum(amount) over (partition by account_id order by paid_at) as running_total
from payments
order by account_id, paid_at
