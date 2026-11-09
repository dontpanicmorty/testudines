select
    campaign_id
  , clicks / nullif(impressions, 0) as ctr
from campaigns
order by campaign_id
