select
    customer_id
  , first_name
  , lower(email) as email_clean
from customers
order by customer_id
