pivot (select product_category, refund_amount from product_returns)
on product_category
using sum(refund_amount)
