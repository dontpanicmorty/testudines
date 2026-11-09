select
    order_id
  , to_json(array_agg(quantity order by product_name)) as quantities_json
from order_items
group by order_id
order by order_id
