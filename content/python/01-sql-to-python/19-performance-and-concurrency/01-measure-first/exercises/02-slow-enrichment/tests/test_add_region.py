import time

from solution import add_region


def test_basic():
    customers = [{"customer_id": 1, "region": "west"}, {"customer_id": 2, "region": "east"}]
    orders = [{"order_id": 10, "customer_id": 2}, {"order_id": 11, "customer_id": 99},
              {"order_id": 12, "customer_id": 1}]
    assert add_region(orders, customers) == [
        {"order_id": 10, "customer_id": 2, "region": "east"},
        {"order_id": 12, "customer_id": 1, "region": "west"},
    ]


def test_does_not_mutate_inputs():
    customers = [{"customer_id": 1, "region": "west"}]
    orders = [{"order_id": 10, "customer_id": 1}]
    add_region(orders, customers)
    assert orders == [{"order_id": 10, "customer_id": 1}]


def test_first_duplicate_customer_wins():
    customers = [{"customer_id": 1, "region": "west"}, {"customer_id": 1, "region": "east"}]
    assert add_region([{"order_id": 1, "customer_id": 1}], customers)[0]["region"] == "west"


def test_empty():
    assert add_region([], []) == []
    assert add_region([{"order_id": 1, "customer_id": 1}], []) == []


def test_scales_linearly():
    n = 8000
    customers = [{"customer_id": i, "region": "r%d" % (i % 5)} for i in range(n)]
    orders = [{"order_id": i, "customer_id": (i * 7) % n} for i in range(n)]
    start = time.perf_counter()
    out = add_region(orders, customers)
    elapsed = time.perf_counter() - start
    assert len(out) == n
    assert elapsed < 0.5, f"took {elapsed:.2f}s for {n} rows: look for a loop inside a loop"
