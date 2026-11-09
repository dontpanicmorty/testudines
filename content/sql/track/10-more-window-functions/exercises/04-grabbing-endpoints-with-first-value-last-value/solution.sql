select
    order_id
  , customer_id
  , order_date
  , amount
  , first_value(amount) over (
      partition by customer_id order by order_date
    ) as first_order_amount
  , last_value(amount) over (
      partition by customer_id order by order_date
      rows between unbounded preceding and unbounded following
    ) as last_order_amount
from orders
order by customer_id, order_date
