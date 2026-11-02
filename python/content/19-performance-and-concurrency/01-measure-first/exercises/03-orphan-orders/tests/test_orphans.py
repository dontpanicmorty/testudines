import time

from solution import orphan_order_ids


def test_basic_dedupe_and_sort():
    orders = [{"order_id": 3, "customer_id": 9}, {"order_id": 1, "customer_id": 1},
              {"order_id": 3, "customer_id": 9}, {"order_id": 2, "customer_id": 8}]
    assert orphan_order_ids(orders, [{"customer_id": 1}]) == [2, 3]


def test_none_customer_is_orphan():
    assert orphan_order_ids([{"order_id": 5, "customer_id": None}], [{"customer_id": 1}]) == [5]


def test_no_orphans():
    assert orphan_order_ids([{"order_id": 1, "customer_id": 1}], [{"customer_id": 1}]) == []


def test_empty_customers_everything_orphan():
    assert orphan_order_ids([{"order_id": 2, "customer_id": 1}, {"order_id": 1, "customer_id": 2}], []) == [1, 2]


def test_empty_orders():
    assert orphan_order_ids([], [{"customer_id": 1}]) == []


def test_returns_list():
    assert isinstance(orphan_order_ids([], []), list)


def test_large_input_is_fast():
    customers = [{"customer_id": i} for i in range(100_000)]
    orders = [{"order_id": i, "customer_id": i % 150_000} for i in range(200_000)]
    start = time.perf_counter()
    out = orphan_order_ids(orders, customers)
    elapsed = time.perf_counter() - start
    expected = sorted({i for i in range(200_000) if i % 150_000 >= 100_000})
    assert out == expected
    assert elapsed < 1.5, f"took {elapsed:.2f}s"
