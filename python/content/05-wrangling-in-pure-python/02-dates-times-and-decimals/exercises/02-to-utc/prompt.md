Events arrive as ISO strings, sometimes with an offset (`2025-06-05T23:30:00+02:00`), sometimes with `Z`, sometimes with no zone (those are known to be UTC already). Write `to_utc(text)` returning an **aware** `datetime` in UTC. Also write `event_day(text)` returning the UTC calendar `date`.

```python
to_utc("2025-06-05T23:30:00+02:00")   # 2025-06-05 21:30:00+00:00
to_utc("2025-06-05T00:48:57")         # 2025-06-05 00:48:57+00:00
event_day("2025-06-06T01:00:00+05:00")  # date(2025, 6, 5)
```
