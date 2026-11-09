Write `import_books(conn, pairs)`. `pairs` is a list of `(title, author_name)` tuples. The function creates these tables if missing:

- `author(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)`
- `book(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author_id INTEGER)`

For every pair it stores the book, linking it to its author's row (adding the author only the first time the name appears). It saves the changes and returns the list of new book ids in order.

```python
import_books(conn, [("Tide Tables", "Aldo"), ("Fen Atlas", "Aldo")])   # [1, 2]
```
