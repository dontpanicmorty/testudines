`apply_corrections(rows, fixes)` should return a corrected copy of `rows` (a list of dicts) and leave `rows` untouched, so the pipeline can compare before and after. `fixes` is a list of `(index, field, new_value)` tuples.

Right now the original data also changes, which breaks the audit step. Fix it.

```python
rows = [{"id": 1, "plan": "free"}, {"id": 2, "plan": "pro"}]
out = apply_corrections(rows, [(0, "plan", "pro")])
out    # [{"id": 1, "plan": "pro"}, {"id": 2, "plan": "pro"}]
rows   # unchanged: [{"id": 1, "plan": "free"}, {"id": 2, "plan": "pro"}]
```
