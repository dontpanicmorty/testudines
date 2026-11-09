select
    c.customer_id
  , c.customer_name
  , to_json(
      array_agg(
        struct_pack(order_id := o.order_id, amount := o.amount)
        order by o.order_id
      )
    ) as orders_json
from customers as c
inner join orders as o
  on c.customer_id = o.customer_id
group by c.customer_id, c.customer_name
order by c.customer_id
