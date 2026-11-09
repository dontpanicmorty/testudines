select
    order_id
  , customer_id
  , amount
from orders
where customer_id in (select customer_id from customers where region = 'west')
order by order_id
