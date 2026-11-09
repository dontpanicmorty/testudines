select customer_id from active_customers
except
select customer_id from feedback_submitters
order by customer_id
