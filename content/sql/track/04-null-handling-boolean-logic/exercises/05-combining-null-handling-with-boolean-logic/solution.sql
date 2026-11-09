select
    lead_id
  , source
  , (converted_at is not null and coalesce(is_qualified, false)) or source = 'referral' as converted_flag
from leads
order by lead_id
