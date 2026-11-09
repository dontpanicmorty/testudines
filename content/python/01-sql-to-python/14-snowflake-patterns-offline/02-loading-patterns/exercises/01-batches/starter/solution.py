from collections.abc import Iterable, Iterator


def batched(items: Iterable, size: int) -> Iterator[list]:
    # TODO: yield lists of up to `size` items
    return [list(items)]
