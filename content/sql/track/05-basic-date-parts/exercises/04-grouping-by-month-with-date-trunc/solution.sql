select
    date_trunc('month', order_date) as order_month
  , sum(amount) as total_amount
from orders
group by date_trunc('month', order_date)
order by order_month
