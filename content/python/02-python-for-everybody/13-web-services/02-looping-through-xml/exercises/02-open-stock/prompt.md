A bike-share feed looks like this:

```xml
<network>
  <station status="open"><bikes>4</bikes></station>
  <station status="closed"><bikes>7</bikes></station>
</network>
```

Write `open_bikes(xml_text)` that returns the total number of bikes (an integer) at stations whose `status` is `"open"`. Closed stations do not count.

```python
# the example above gives 4
```
