Build a small read API over an in-memory customer list.

Write `create_app(customers)` returning a `FastAPI` app. `customers` is a list of dicts like `{"customer_id": 1, "name": "Ada", "region": "west"}`.

- `GET /customers/{customer_id}`: the customer dict, `404` if absent, `422` if the id is not an integer.
- `GET /customers?region=west&limit=10&offset=0`: a JSON object `{"items": [...], "total": N}` where `total` is the count **after** the region filter and `items` is the page. `limit` defaults to 10 and must be 1..100, `offset` defaults to 0 and must be >= 0, otherwise `422`. Without `region`, no filtering.

```python
client = TestClient(create_app(rows))
client.get("/customers/2").json()
client.get("/customers?region=west&limit=1").json()  # {"items": [...], "total": 3}
```
