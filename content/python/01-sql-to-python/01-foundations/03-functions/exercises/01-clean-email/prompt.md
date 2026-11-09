Write `clean_email(email)` with a one-line docstring. It should return the email stripped of whitespace and lowercased. If the result is empty, or `email` is `None`, return `None`. It must **return**, not print.

```python
clean_email("  Ada@Example.COM ")  # "ada@example.com"
clean_email("   ")                 # None
clean_email(None)                  # None
```
