select
    ticket_id
  , upper(replace(description, '{{customer}}', 'the customer')) as description
from support_tickets
order by ticket_id
