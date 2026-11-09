A feed arrives as text, one `station,bikes` pair per line. Some lines are bad: blank, missing a comma, or with a bike count that is not a whole number.

Write `load_feed(db_path, text)`. Create table `reading(station TEXT, bikes INTEGER)` if needed, insert every good line, save, and return a tuple `(inserted, skipped)`. Blank lines are neither inserted nor counted as skipped.

```python
load_feed("x.db", "Mill Lane,4\nbad line\nHill Top,nine\n")   # (1, 2)
```
