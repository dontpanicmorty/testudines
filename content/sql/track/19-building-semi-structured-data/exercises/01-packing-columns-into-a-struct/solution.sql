select
    customer_id
  , struct_pack(first_name := first_name, last_name := last_name, email := email) as contact_info
from customers
order by customer_id
