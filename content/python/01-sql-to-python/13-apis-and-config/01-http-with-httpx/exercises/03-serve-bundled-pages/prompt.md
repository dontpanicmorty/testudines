The data directory holds `api_users_page1.json`, `api_users_page2.json`, ... Each file looks like `{"page": 1, "results": [{"id", "name", "active"}], "next": 2}` (`next` is `null` on the last page).

Write two functions:

1. `make_mock_client(data_dir)` returns an `httpx.Client` (base URL `https://api.example.test`) backed by `httpx.MockTransport`. `GET /users?page=N` serves the matching file as a 200 JSON response. A page with no file gets a `404` with body `{"error": "not found"}`. Any other path is also a 404.
2. `active_names(client)` starts at page 1, follows each response's `next` until it is `None`, and returns the names of users with `active == true`, in order.

```python
client = make_mock_client(Path("datasets"))
client.get("/users", params={"page": 1}).json()["page"]   # 1
active_names(client)                                       # ["Frances Clarke", ...]
```

You may use `Path.read_text()` and `json`. `data_dir` is a `pathlib.Path`.
