A weather feed sends a small XML document for one town. Write `town_name(xml_text)` that returns the text of the `<name>` child of the root element.

```python
town_name("<town><name>Larkfield</name><pop>900</pop></town>")   # "Larkfield"
```
