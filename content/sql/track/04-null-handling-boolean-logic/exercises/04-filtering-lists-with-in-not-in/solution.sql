select
    event_id
  , event_type
from events
where event_type in ('signup', 'upgrade', 'renewal')
order by event_id
