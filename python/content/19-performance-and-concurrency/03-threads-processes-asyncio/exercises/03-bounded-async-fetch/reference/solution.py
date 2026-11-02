import asyncio
from typing import Awaitable, Callable, Iterable


async def fetch_many(fetch: Callable[[int], Awaitable], ids: Iterable[int], limit: int = 5) -> list:
    if limit < 1:
        raise ValueError("limit must be >= 1")
    sem = asyncio.Semaphore(limit)

    async def guarded(i: int):
        async with sem:
            return await fetch(i)

    return list(await asyncio.gather(*(guarded(i) for i in ids)))
