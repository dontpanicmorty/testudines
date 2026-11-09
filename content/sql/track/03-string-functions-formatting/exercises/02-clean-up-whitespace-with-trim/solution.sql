select
    customer_id
  , trim(raw_name) as clean_name
from customers
order by customer_id
