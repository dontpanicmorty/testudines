A feed groups stations into zones:

```xml
<city>
  <zone name="North"><station>Mill Lane</station><station>Hill Top</station></zone>
  <zone name="South"><station>Quay Street</station></zone>
</city>
```

Write `stations_by_zone(xml_text)` that returns a dictionary mapping each zone's name to the list of its station names (in document order). Zones with no stations map to an empty list.

```python
{"North": ["Mill Lane", "Hill Top"], "South": ["Quay Street"]}
```
