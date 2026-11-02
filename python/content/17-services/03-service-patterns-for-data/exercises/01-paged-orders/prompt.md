Write `create_app(db_path)` returning a FastAPI app that reads an sqlite file with table `orders(order_id INTEGER, customer_id INTEGER, status TEXT)`.

`GET /orders?page=1&page_size=10&status=shipped` returns

```json
{"items": [{"order_id": 1, "customer_id": 5, "status": "shipped"}], "page": 1, "page_size": 10, "total": 25, "has_next": true}
```

- Items are ordered by `order_id` ascending.
- `status` is optional; when given, only matching rows are returned and `total` counts only those.
- `page` defaults to 1 (min 1); `page_size` defaults to 10 (1..50). Violations give `422`.
- `has_next` is true when more rows exist after this page.
- Open a **fresh connection per request** and close it. Use `?` placeholders, never string-formatted SQL.

`GET /health` returns `{"status": "ok"}` after running `select 1`, or `503` with `{"status": "down"}` if the query raises.
