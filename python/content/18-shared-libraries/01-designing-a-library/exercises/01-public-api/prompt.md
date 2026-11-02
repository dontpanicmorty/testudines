The `fmtkit` package has two useful functions, `clean_name` and `parse_amount`, but consumers have to import them from `fmtkit.core`, and a helper called `normalize` is leaking as if it were public.

Shape the public API:

- `from fmtkit import clean_name, parse_amount` works.
- `fmtkit.__all__` contains exactly those two names.
- The helper is private: it is named `_normalize` in `fmtkit/core.py` and `fmtkit/core.py` no longer has a public `normalize`.
- `from fmtkit import *` must expose only the two functions.

```python
from fmtkit import clean_name, parse_amount
clean_name("  ada   LOVELACE ")   # "Ada Lovelace"
parse_amount("$1,234.50")         # 1234.5
```

Edit `fmtkit/__init__.py` and `fmtkit/core.py`.
