Write `error_name(action)`. The argument `action` is a function that takes no arguments. Call it. If it runs without any error, return `"none"`. If it raises an exception, return the exception's name as text, such as `"ValueError"`.

```python
error_name(lambda: 10 / 0)       # "ZeroDivisionError"
error_name(lambda: int("abc"))   # "ValueError"
error_name(lambda: 1 + 1)        # "none"
```
