Define `Book` with a constructor taking `title` and `pages`.

- `read(n)` moves the reader forward `n` pages but never beyond the last page.
- `pages_left()` returns how many pages remain.
- `percent()` returns the progress as an integer percentage, rounded to the nearest whole number (use `round`).
- `str(book)` gives `"<title> (<page>/<pages>)"`.

```python
b = Book("Tide Tables", 200)
b.read(30)
str(b)         # "Tide Tables (30/200)"
b.percent()    # 15
```
