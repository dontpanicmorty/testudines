select
    order_id
  , order_date
  , amount
from orders
where extract(month from order_date) = 4
order by order_date
