A users API returns JSON like `{"page": 1, "results": [{"id": 1, "name": "..."}], "next": 2}`.

Write `fetch_users_page(client, page)` that calls `GET /users` with the query parameter `page`, raises `httpx.HTTPStatusError` for any non-2xx response, and returns the **list** under `"results"`.

```python
client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")
fetch_users_page(client, 1)   # [{"id": 1, "name": "Ada"}, ...]
```

The client is passed in, so tests can supply a fake one.
