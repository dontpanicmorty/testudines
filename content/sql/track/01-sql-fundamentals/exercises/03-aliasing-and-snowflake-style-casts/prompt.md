This codebase leans heavily on Snowflake's `::type` shorthand instead of `CAST(x AS type)`.

From `orders`, return `order_id`, the `amount` cast to an integer (rounded to the nearest dollar) aliased as `amount_whole_dollars`, and `order_date` cast to a string aliased as `order_date_string`.

Order by `order_id`.
