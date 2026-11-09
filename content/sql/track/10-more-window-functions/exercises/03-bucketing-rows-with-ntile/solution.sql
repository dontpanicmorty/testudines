select
    customer_id
  , lifetime_value
  , ntile(4) over (order by lifetime_value desc) as value_quartile
from customers
order by customer_id
