A help desk gives tickets codes made of **two capital letters, a dash, and one or more digits**, for example `AB-7` or `QX-20481`. Write `is_ticket(text)` that returns `True` only when the **entire** text is a code of that shape.

```python
is_ticket("AB-7")        # True
is_ticket("ab-7")        # False
is_ticket("AB-")         # False
is_ticket("xAB-7")       # False
```
