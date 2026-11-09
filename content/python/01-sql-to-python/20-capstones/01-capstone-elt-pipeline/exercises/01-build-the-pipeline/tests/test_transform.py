from pipeline.transform import daily_revenue


def order(oid, cid, ts, status="completed"):
    return {"order_id": oid, "customer_id": cid, "placed_at": ts, "status": status}


def item(oid, qty, price, pid="P1"):
    return {"order_id": oid, "product_id": pid, "quantity": qty, "unit_price": price}


CUSTOMERS = [{"customer_id": 1, "region": "west"}, {"customer_id": 2, "region": "east"}]


def test_basic_grouping_and_rounding():
    orders = [order(1, 1, "2025-01-01 09:00:00"), order(2, 1, "2025-01-01 18:00:00")]
    items = [item(1, 3, 0.1), item(2, 1, 0.2), item(2, 1, 0.1)]
    out = daily_revenue(orders, items, CUSTOMERS)
    assert out == [{"day": "2025-01-01", "region": "west", "orders": 2, "revenue": 0.6}]


def test_only_completed_and_shipped_count():
    orders = [order(1, 1, "2025-01-01 09:00:00", "cancelled"), order(2, 1, "2025-01-01 09:00:00", "refunded"),
              order(3, 1, "2025-01-01 09:00:00", "shipped")]
    items = [item(1, 1, 100), item(2, 1, 100), item(3, 1, 5)]
    out = daily_revenue(orders, items, CUSTOMERS)
    assert out == [{"day": "2025-01-01", "region": "west", "orders": 1, "revenue": 5.0}]


def test_sorted_by_day_then_region():
    orders = [order(1, 2, "2025-01-02 09:00:00"), order(2, 1, "2025-01-01 09:00:00"),
              order(3, 2, "2025-01-01 09:00:00")]
    items = [item(1, 1, 1), item(2, 1, 1), item(3, 1, 1)]
    out = daily_revenue(orders, items, CUSTOMERS)
    assert [(r["day"], r["region"]) for r in out] == [
        ("2025-01-01", "east"), ("2025-01-01", "west"), ("2025-01-02", "east")]


def test_unknown_customer_region():
    out = daily_revenue([order(1, 99, "2025-01-01 09:00:00")], [item(1, 2, 3)], CUSTOMERS)
    assert out == [{"day": "2025-01-01", "region": "unknown", "orders": 1, "revenue": 6.0}]


def test_order_without_items_counts_with_zero_revenue():
    out = daily_revenue([order(1, 1, "2025-01-01 09:00:00")], [], CUSTOMERS)
    assert out == [{"day": "2025-01-01", "region": "west", "orders": 1, "revenue": 0.0}]


def test_items_for_unknown_orders_ignored():
    out = daily_revenue([order(1, 1, "2025-01-01 09:00:00")], [item(1, 1, 1), item(500, 9, 9)], CUSTOMERS)
    assert out[0]["revenue"] == 1.0


def test_empty():
    assert daily_revenue([], [], []) == []


def test_pure_inputs_not_mutated():
    orders = [order(1, 1, "2025-01-01 09:00:00")]
    items = [item(1, 1, 1)]
    before = (list(map(dict, orders)), list(map(dict, items)))
    daily_revenue(orders, items, CUSTOMERS)
    assert (orders, items) == before
