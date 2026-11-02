Write `try_int(value, default=None)`: return `int(value)` when it converts, otherwise `default`. It must handle strings with surrounding spaces, `None`, and floats-as-text like `"3.5"` (which is **not** an int, so returns the default).

```python
try_int(" 42 ")          # 42
try_int("3.5", -1)       # -1
try_int(None)            # None
```
