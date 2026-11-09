from typing import Awaitable, Callable, Iterable


async def fetch_many(fetch: Callable[[int], Awaitable], ids: Iterable[int], limit: int = 5) -> list:
    if limit < 1:
        raise ValueError("limit must be >= 1")
    results = []
    for i in ids:
        results.append(await fetch(i))
    return results
