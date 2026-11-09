select
    product_id
  , effective_date
  , count(*) as row_count
from price_history
group by product_id, effective_date
having count(*) > 1
order by product_id, effective_date
