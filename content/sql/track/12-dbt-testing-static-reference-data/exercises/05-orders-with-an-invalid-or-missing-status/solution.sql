select
    o.order_id
  , o.amount
  , l.status_label
  , l.status_code is null or not coalesce(l.is_valid_status, false) as fails_accepted_values
from orders as o
left join status_lookup as l
  on o.status_code = l.status_code
order by o.order_id
