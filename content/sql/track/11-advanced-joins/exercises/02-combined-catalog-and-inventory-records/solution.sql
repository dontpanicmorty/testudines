select
    coalesce(c.product_id, i.product_id) as product_id
  , c.product_name
  , i.quantity_on_hand
from product_catalog as c
full outer join inventory as i
  on c.product_id = i.product_id
order by product_id
