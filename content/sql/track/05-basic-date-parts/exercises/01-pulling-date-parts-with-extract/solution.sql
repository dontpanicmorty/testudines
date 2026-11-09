select
    order_id
  , extract(year from order_date) as order_year
  , extract(month from order_date) as order_month
from orders
order by order_id
