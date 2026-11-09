`mylib/transform.py` worked fine while the author ran it from inside the `mylib/` folder. Now that it's part of a real package, `from mylib.transform import normalize_rows` fails with a `ModuleNotFoundError`.

Fix the imports so that the package imports correctly from the project root, without moving files or copying code.

```python
from mylib.transform import normalize_rows
normalize_rows([{"name": " ada ", "email": "ADA@X.COM"}])
# [{'name': 'Ada', 'email': 'ada@x.com'}]
```
