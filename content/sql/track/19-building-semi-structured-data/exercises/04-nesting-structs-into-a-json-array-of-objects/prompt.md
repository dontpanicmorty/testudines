Go one level deeper: for each `order_id`, build a JSON array where each element is an object containing that item's `product_name` and `quantity` (not just the raw quantity). Order the elements within each array by `product_name` for a deterministic result. Return `order_id` and `items_json`.

Order by `order_id`.
