select
    customer_id
  , sum(case when channel = 'online' then amount else 0 end) as online_total
  , sum(case when channel = 'retail' then amount else 0 end) as retail_total
from orders
group by customer_id
order by customer_id
