select
    signup_date
  , signup_count
  , avg(signup_count) over (
      order by signup_date
      rows between 2 preceding and current row
    ) as moving_avg
from daily_signups
order by signup_date
