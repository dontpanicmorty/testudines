The table is `products(product_id INTEGER, name TEXT, category TEXT, unit_price REAL)`.

Write `search_products(conn, category=None, min_price=None, sort_by="name", direction="asc")` returning a list of dicts (`product_id`, `name`, `category`, `unit_price`).

- `category`, if given, filters by exact match; `min_price`, if given, keeps `unit_price >= min_price`. Either, both or neither may be given.
- `sort_by` must be one of `product_id`, `name`, `category`, `unit_price`; `direction` must be `asc` or `desc` (any case). Otherwise raise `ValueError`.
- Values must be passed as parameters.

```python
search_products(conn, category="tools", min_price=10, sort_by="unit_price", direction="desc")
```
