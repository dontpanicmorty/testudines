A list of text lines should each look like `name,lat,lon`. Write `clean_places(lines)` returning a list of dictionaries `{"name": str, "lat": float, "lon": float}` for the valid lines, in order. Drop a line if it does not have exactly three comma-separated parts, if lat or lon is not a number, if lat is outside -90..90, or if lon is outside -180..180. Strip spaces around each part. Blank lines are dropped too.

```python
clean_places(["Larkfield, 51.2, -1.4", "Nowhere,n/a,5"])
# [{"name": "Larkfield", "lat": 51.2, "lon": -1.4}]
```
