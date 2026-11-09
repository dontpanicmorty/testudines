Write `internal_links(html, known)`. `html` is a string of HTML. `known` is a set of page names that belong to the site. Return a sorted list of the unique link targets (the value of each `href="..."`) that appear in `known`. Links elsewhere are ignored.

```python
internal_links('<a href="b.html">B</a><a href="https://x.test">X</a><a href="b.html">again</a>', {"a.html", "b.html"})
# ["b.html"]
```
