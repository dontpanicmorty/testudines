A sensor sends a reading like this:

```xml
<reading sensor="T3"><temp unit="C">21.5</temp></reading>
```

Write `parse_reading(xml_text)` that returns a tuple `(sensor, value, unit)`, where `sensor` and `unit` are strings and `value` is a float.

```python
parse_reading('<reading sensor="T3"><temp unit="C">21.5</temp></reading>')
# ("T3", 21.5, "C")
```
