import time
from typing import Callable


def best_of(fn: Callable[[], object], number: int = 1000, repeat: int = 5,
            timer: Callable[[], float] = time.perf_counter) -> float:
    raise NotImplementedError
