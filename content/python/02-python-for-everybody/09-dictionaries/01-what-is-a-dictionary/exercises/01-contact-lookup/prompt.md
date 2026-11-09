You are given a dictionary that maps names to phone numbers. Write `find_number(book, name)` that returns the number stored for `name`. If the name is not in the book, return the text `"unknown"` instead of crashing.

```python
book = {"Maya": "555-0101"}
find_number(book, "Maya")    # "555-0101"
find_number(book, "Priya")   # "unknown"
```
