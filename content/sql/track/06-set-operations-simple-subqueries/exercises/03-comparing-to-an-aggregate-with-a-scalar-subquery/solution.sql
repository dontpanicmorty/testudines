select
    order_id
  , customer_id
  , amount
from orders
where amount > (select avg(amount) from orders)
order by order_id
