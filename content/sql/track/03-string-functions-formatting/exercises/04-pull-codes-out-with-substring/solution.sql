select
    product_id
  , sku
  , substring(sku, 1, 4) as category_code
from products
order by product_id
