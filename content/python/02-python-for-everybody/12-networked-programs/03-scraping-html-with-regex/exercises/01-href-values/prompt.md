Write `link_targets(html)` that returns a list of the link addresses found in an HTML string: the text inside the double quotes of every `href="..."`, in order of appearance. Assume the pages use double quotes and lowercase `href`.

```python
link_targets('<a href="/a">A</a> <a href="/b">B</a>')    # ["/a", "/b"]
```
