with daily_totals as (
    select
        sale_date
      , sum(case when channel = 'online' then amount else 0 end) as online_total
      , sum(case when channel = 'retail' then amount else 0 end) as retail_total
    from daily_sales
    group by sale_date
)
select
    sale_date
  , online_total
  , retail_total
  , sum(online_total) over (
      order by sale_date
      rows between 2 preceding and current row
    ) as trailing_online_3day
from daily_totals
order by sale_date
