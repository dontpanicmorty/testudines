`create_customer(store, body)` models `POST /customers`. `store` is a dict of `customer_id -> customer`. It should behave like this:

- body must contain a non-empty `name` and an `email` containing `@`; otherwise return `(422, {"error": ...})`
- emails are compared case-insensitively and ignoring surrounding spaces; a customer whose email already exists gives `(409, {"error": ...})` and the store is unchanged
- on success the customer gets the next integer id (max existing id + 1, or 1 for an empty store), is saved with a normalised (stripped, lowercased) email, and the handler returns `(201, <the saved customer>)`

```python
store = {}
create_customer(store, {"name": "Ada", "email": " Ada@Example.com "})
# (201, {"id": 1, "name": "Ada", "email": "ada@example.com"})
create_customer(store, {"name": "Ada Two", "email": "ADA@example.com"})
# (409, {"error": "..."})
```

The version in `solution.py` is wrong: bad emails get saved, duplicates slip in, and the status codes are off. Fix it.
