Write `report_load(table, loaded, rejected)` using a module-level logger named `__name__`.

- Always log at INFO: `loaded table=<table> rows=<loaded>`.
- If `rejected > 0`, also log at WARNING: `rejected table=<table> rows=<rejected>`.
- Use a logger, not `print`.

```python
report_load("orders", 1204, 12)
# INFO    loaded table=orders rows=1204
# WARNING rejected table=orders rows=12
```
