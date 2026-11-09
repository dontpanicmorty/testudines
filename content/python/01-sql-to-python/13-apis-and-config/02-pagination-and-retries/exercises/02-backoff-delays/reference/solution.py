"""Exponential backoff schedule with optional full jitter."""
import random


def backoff_delays(retries: int, base: float = 0.5, cap: float = 8.0,
                   rng: random.Random | None = None) -> list[float]:
    if base < 0 or cap < 0:
        raise ValueError("base and cap must be non-negative")
    delays: list[float] = []
    for attempt in range(max(retries, 0)):
        ceiling = min(cap, base * 2 ** attempt)
        delays.append(rng.uniform(0, ceiling) if rng is not None else ceiling)
    return delays
