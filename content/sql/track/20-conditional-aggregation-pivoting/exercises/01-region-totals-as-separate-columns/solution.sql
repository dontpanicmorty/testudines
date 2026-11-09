select
    sum(case when region = 'west' then amount else 0 end) as west_total
  , sum(case when region = 'east' then amount else 0 end) as east_total
  , sum(case when region = 'north' then amount else 0 end) as north_total
from orders
