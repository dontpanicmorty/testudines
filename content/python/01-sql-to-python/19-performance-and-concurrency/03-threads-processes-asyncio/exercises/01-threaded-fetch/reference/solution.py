from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Sequence, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def fetch_all(fetch: Callable[[T], R], ids: Sequence[T], max_workers: int = 8) -> list[R]:
    if max_workers < 1:
        raise ValueError("max_workers must be >= 1")
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(fetch, ids))
