Schemas are dicts `{column: type_name}`. Write three functions.

`diff_schemas(old, new)` returns `{"added": [...], "removed": [...], "retyped": {col: (old_type, new_type)}}`, with `added` and `removed` sorted and `retyped` including only columns present in both whose type differs.

`is_backward_compatible(old, new)` is `True` unless a column was removed or retyped, where `int` -> `float` is the one allowed retype (widening). Added columns are compatible.

`next_version(version, old, new)` takes a `"major.minor.patch"` string and returns the contract's next version: **major** +1 (minor, patch reset to 0) if not compatible; otherwise **minor** +1 (patch reset) if anything changed (added column or widening); otherwise the same version unchanged.

```python
next_version("1.4.2", {"a": "int"}, {"a": "int", "b": "str"})   # "1.5.0"
```
