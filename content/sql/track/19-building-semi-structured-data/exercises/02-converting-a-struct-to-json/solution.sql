select
    order_id
  , to_json(
      struct_pack(order_id := order_id, amount := amount, status := status)
    ) as order_json
from orders
order by order_id
