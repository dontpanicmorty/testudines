select customer_id from webinar_attendees
intersect
select customer_id from email_clickers
order by customer_id
