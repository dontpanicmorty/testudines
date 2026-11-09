select
    sale_date
  , region
  , amount
  , sum(amount) over (
      partition by region order by sale_date
      rows between 2 preceding and current row
    ) as trailing_3day_total
from daily_sales
order by region, sale_date
