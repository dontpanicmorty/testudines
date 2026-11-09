import asyncio
import time

import pytest

from solution import fetch_many


def make_fetch(delay=0.05):
    state = {"now": 0, "peak": 0}

    async def fetch(i):
        state["now"] += 1
        state["peak"] = max(state["peak"], state["now"])
        await asyncio.sleep(delay)
        state["now"] -= 1
        return i * 2

    return fetch, state


def run(coro):
    return asyncio.run(coro)


def test_results_in_order():
    fetch, _ = make_fetch(0.01)
    assert run(fetch_many(fetch, range(10), limit=4)) == [i * 2 for i in range(10)]


def test_is_concurrent():
    fetch, _ = make_fetch(0.05)
    start = time.perf_counter()
    run(fetch_many(fetch, range(20), limit=10))
    elapsed = time.perf_counter() - start
    assert elapsed < 0.5, f"{elapsed:.2f}s: calls look sequential (serial would be about 1.0s)"


def test_limit_is_respected_and_reached():
    fetch, state = make_fetch(0.02)
    run(fetch_many(fetch, range(20), limit=4))
    assert state["peak"] <= 4, f"peak concurrency {state['peak']}"
    assert state["peak"] >= 2, "calls never overlapped"


def test_limit_one_is_sequential():
    fetch, state = make_fetch(0.005)
    run(fetch_many(fetch, range(5), limit=1))
    assert state["peak"] == 1


def test_empty():
    fetch, _ = make_fetch()
    assert run(fetch_many(fetch, [], limit=3)) == []


def test_invalid_limit():
    fetch, _ = make_fetch()
    with pytest.raises(ValueError):
        run(fetch_many(fetch, [1], limit=0))


def test_exception_propagates():
    async def fetch(i):
        await asyncio.sleep(0.001)
        if i == 3:
            raise RuntimeError("bad id")
        return i

    with pytest.raises(RuntimeError):
        run(fetch_many(fetch, range(6), limit=3))


def test_semaphore_not_shared_across_runs():
    fetch, _ = make_fetch(0.001)
    assert run(fetch_many(fetch, range(3), limit=2)) == [0, 2, 4]
    assert run(fetch_many(fetch, range(3), limit=2)) == [0, 2, 4]
