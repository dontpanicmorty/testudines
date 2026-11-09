select
    event_id
  , date_trunc('month', occurred_at) as event_month
from events
order by event_id
