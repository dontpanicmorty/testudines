Define a type called `Tally` for counting visitors.

- `Tally()` starts at 0 and exposes the current number as `count`.
- `add(n=1)` increases the count by `n`.
- `reset()` sets it back to 0.

```python
t = Tally()
t.add()
t.add(4)
t.count      # 5
```
