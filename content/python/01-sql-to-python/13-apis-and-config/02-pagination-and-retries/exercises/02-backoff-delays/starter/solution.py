"""Exponential backoff schedule with optional full jitter."""
import random


def backoff_delays(retries: int, base: float = 0.5, cap: float = 8.0,
                   rng: random.Random | None = None) -> list[float]:
    ...
