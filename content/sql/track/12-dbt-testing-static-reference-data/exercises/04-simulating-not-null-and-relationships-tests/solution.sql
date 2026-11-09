select
    order_id
from orders
where customer_id is null
   or customer_id not in (select customer_id from customers)
order by order_id
