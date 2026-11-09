select
    o.order_id
  , o.amount
  , l.status_label
from orders as o
inner join status_lookup as l
  on o.status_code = l.status_code
order by o.order_id
