A monitoring system writes lines such as `ERROR: disk full` or `INFO: all good`. Write `is_alarm(line)` that returns `True` when the line **begins** with the word `ERROR` followed by a colon, and `False` otherwise. Case matters, and `ERROR` in the middle of a line does not count.

```python
is_alarm("ERROR: disk full")    # True
is_alarm("see ERROR: later")    # False
```
