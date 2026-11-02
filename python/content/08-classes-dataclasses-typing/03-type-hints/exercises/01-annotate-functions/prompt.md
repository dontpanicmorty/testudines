`solution.py` works at runtime but has no annotations, so `python -m mypy --strict solution.py` fails. Add type hints (don't change behaviour) so that:

- `total_cents` takes a list of floats and returns an `int`;
- `first_or_none` takes a list of any element type and returns that element type or `None`;
- `group_by_region` takes a list of `dict[str, str]` rows and returns `dict[str, list[str]]`.

```python
total_cents([1.10, 2.20])                                   # 330
first_or_none(["a", "b"])                                   # 'a'
group_by_region([{"region": "EU", "customer_id": "7"}])     # {'EU': ['7']}
```

The check runs `mypy --strict` on your file *and* on a small caller that depends on the exact signatures. Don't use `Any` or `# type: ignore`.
