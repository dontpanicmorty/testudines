from typing import Callable, Sequence, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def fetch_all(fetch: Callable[[T], R], ids: Sequence[T], max_workers: int = 8) -> list[R]:
    raise NotImplementedError
