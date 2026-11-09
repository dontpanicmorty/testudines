Write `headings(html)` that returns the text of every first-level and second-level heading (`<h1>...</h1>` and `<h2>...</h2>`, no attributes) in order, with leading and trailing spaces removed. Headings never contain other tags in these pages and never span several lines.

```python
headings("<h1> Club </h1><p>x</p><h2>News</h2>")    # ["Club", "News"]
```
