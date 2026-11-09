select customer_id from customers where region = 'west'
except
select customer_id from orders
order by customer_id
