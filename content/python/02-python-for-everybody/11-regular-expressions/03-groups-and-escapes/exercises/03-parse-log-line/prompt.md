A service writes lines like `2026-03-01 14:22:05 [WARN] cache is cold`: a date, a time, a level in square brackets (capital letters), then the message. Write `parse_line(line)` that returns a dictionary with the keys `"date"`, `"time"`, `"level"` and `"message"`, all text. If the line does not fit this format exactly, return `None`. The message is everything after the single space that follows the level, and cannot be empty.

```python
parse_line("2026-03-01 14:22:05 [WARN] cache is cold")
# {"date": "2026-03-01", "time": "14:22:05", "level": "WARN", "message": "cache is cold"}
```
