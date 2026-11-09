Write `backoff_delays(retries, base=0.5, cap=8.0, rng=None)` returning a list of `retries` wait times in seconds, one per retry.

- The ceiling for retry `i` (starting at 0) is `min(cap, base * 2**i)`.
- If `rng` is `None`, return the ceilings (no jitter).
- If `rng` (a `random.Random`) is given, return `rng.uniform(0, ceiling)` for each retry, drawing in order. This is "full jitter" and is reproducible with a seeded generator.
- `retries <= 0` returns `[]`. A negative `base` or `cap` raises `ValueError`.

```python
backoff_delays(6)                         # [0.5, 1.0, 2.0, 4.0, 8.0, 8.0]
backoff_delays(3, rng=random.Random(1))   # three values, each <= its ceiling
```
