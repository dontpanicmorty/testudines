`emails.clean_email(raw)` normalises e-mail addresses from a sign-up form:

- strips surrounding whitespace and lower-cases the address;
- returns `None` for `None`, blank input, or an invalid address, meaning not exactly one `@` with text on both sides.

Write a **parametrized** test table in `my_tests.py` that passes on the real function and catches every hidden-bug variant.

```python
from emails import clean_email
clean_email("  Ada@Example.COM ")   # "ada@example.com"
clean_email("no-at-sign")           # None
clean_email(None)                   # None
```

Your file must use `parametrize` and contain at least 8 cases.
