import threading
import time

import pytest

from solution import fetch_all


def slow(i):
    time.sleep(0.05)
    return i * 10


def test_results_in_input_order():
    ids = list(range(12))
    assert fetch_all(slow, ids, max_workers=6) == [i * 10 for i in ids]


def test_actually_concurrent():
    start = time.perf_counter()
    fetch_all(slow, list(range(20)), max_workers=10)
    elapsed = time.perf_counter() - start
    assert elapsed < 0.6, f"{elapsed:.2f}s; serial would be about 1.0s"


def test_uses_multiple_threads():
    names = set()

    def f(i):
        names.add(threading.current_thread().name)
        time.sleep(0.02)
        return i

    fetch_all(f, list(range(8)), max_workers=4)
    assert len(names) > 1


def test_max_workers_respected():
    lock = threading.Lock()
    state = {"now": 0, "peak": 0}

    def f(i):
        with lock:
            state["now"] += 1
            state["peak"] = max(state["peak"], state["now"])
        time.sleep(0.02)
        with lock:
            state["now"] -= 1
        return i

    fetch_all(f, list(range(12)), max_workers=3)
    assert state["peak"] <= 3


def test_exception_propagates():
    def f(i):
        if i == 2:
            raise KeyError("boom")
        return i

    with pytest.raises(KeyError):
        fetch_all(f, [1, 2, 3], max_workers=2)


def test_empty_and_invalid():
    assert fetch_all(slow, [], max_workers=2) == []
    with pytest.raises(ValueError):
        fetch_all(slow, [1], max_workers=0)
