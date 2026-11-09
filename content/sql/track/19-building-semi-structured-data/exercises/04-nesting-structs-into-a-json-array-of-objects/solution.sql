select
    order_id
  , to_json(
      array_agg(
        struct_pack(product_name := product_name, quantity := quantity)
        order by product_name
      )
    ) as items_json
from order_items
group by order_id
order by order_id
