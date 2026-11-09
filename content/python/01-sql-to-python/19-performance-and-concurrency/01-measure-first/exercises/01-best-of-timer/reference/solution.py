import time
from typing import Callable


def best_of(fn: Callable[[], object], number: int = 1000, repeat: int = 5,
            timer: Callable[[], float] = time.perf_counter) -> float:
    if number < 1 or repeat < 1:
        raise ValueError("number and repeat must be >= 1")
    runs = []
    for _ in range(repeat):
        start = timer()
        for _ in range(number):
            fn()
        runs.append(timer() - start)
    return min(runs) / number
