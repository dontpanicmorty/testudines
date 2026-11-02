`ENVIRONMENTS` holds the database, warehouse and role for each environment. Write `environment_params(name, *, allow_prod=False)`:

- returns a **copy** of that environment's dict (callers add keys to it; the shared table must never change);
- an unknown name raises `ValueError` whose message lists the valid names;
- `"prod"` raises `PermissionError` unless `allow_prod=True`.

```python
environment_params("dev")                    # {"database": "ANALYTICS_DEV", "warehouse": "DEV_WH", "role": "LOADER_DEV"}
environment_params("prod", allow_prod=True)
environment_params("prod")                   # PermissionError
```
