Build `POST /orders` with validation, in `create_app()` returning a `FastAPI` app.

Request body:

```json
{"customer_id": 7, "items": [{"sku": "P003", "quantity": 2, "unit_price": 10.5}]}
```

Rules (violations must give `422`, with no code of your own for the checks):
- `customer_id` is an int, `items` has at least one entry
- each item has a non-empty `sku` string, `quantity` an int > 0, `unit_price` a number > 0

On success respond `201` with exactly `{"order_id": N, "customer_id": 7, "total": 21.0}`. `order_id` starts at 1 and increases with each created order in that app. `total` is the sum of `quantity * unit_price`, rounded to 2 places. Invalid requests must **not** consume an order id.

Also add `GET /orders/{order_id}` returning the same shape, or `404` if unknown.
