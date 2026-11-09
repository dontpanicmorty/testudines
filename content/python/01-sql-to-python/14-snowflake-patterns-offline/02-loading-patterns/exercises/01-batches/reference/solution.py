from collections.abc import Iterable, Iterator
from itertools import islice


def batched(items: Iterable, size: int) -> Iterator[list]:
    if size < 1:
        raise ValueError("size must be >= 1")
    it = iter(items)
    while chunk := list(islice(it, size)):
        yield chunk
