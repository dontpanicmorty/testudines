Add a computed column `business_tier` to `orders` that labels each order:
- 'large' when amount >= 100
- 'medium' when amount >= 50
- otherwise 'small'

Return `order_id`, `amount`, `business_tier`, ordered by `order_id`.
