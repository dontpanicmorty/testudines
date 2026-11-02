`users_api.fetch_all_users(client)` collects users from a paginated API. The client has one method, `get_page(n)`, returning `{"users": [...], "next_page": int | None}`.

Contract:

- start at page **1**, follow `next_page` until it is `None`;
- return all users, in order, across pages (including the last page);
- if the client raises `ConnectionError`, raise `users_api.FetchError` instead (with the original error as its cause).

Write `my_tests.py` using your own fake client (no network, no real API). It must pass on the real function and catch every hidden-bug variant.

```python
from users_api import fetch_all_users, FetchError
fetch_all_users(client)   # [{"id": 1}, {"id": 2}, {"id": 3}]
```

Write at least 3 tests.
