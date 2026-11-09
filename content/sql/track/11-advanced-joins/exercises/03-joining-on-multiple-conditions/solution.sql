select
    s.shipment_id
  , s.warehouse_code
  , s.shipped_at
  , r.rate_per_unit
from shipments as s
inner join warehouse_rates as r
  on s.warehouse_code = r.warehouse_code
 and extract(year from s.shipped_at) = r.effective_year
order by s.shipment_id
