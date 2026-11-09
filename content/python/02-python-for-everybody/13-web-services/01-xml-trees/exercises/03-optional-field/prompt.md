Some records in a feed leave out fields. Write `field_or_default(xml_text, tag, default)` that returns the text of the first child of the root with the given tag name. If there is no such child, or the child is empty, return `default` instead.

```python
field_or_default("<a><b>hi</b></a>", "b", "?")     # "hi"
field_or_default("<a><b>hi</b></a>", "c", "?")     # "?"
field_or_default("<a><b></b></a>", "b", "?")       # "?"
```
