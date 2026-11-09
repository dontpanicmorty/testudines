import copy
from solution import enrich_orders


def test_join_and_left_semantics():
    orders = [{"order_id": 1, "customer_id": "c1", "amount": 9.0},
              {"order_id": 2, "customer_id": "zz", "amount": 5.0}]
    customers = [{"customer_id": "c1", "region": "EU", "plan": "pro"}]
    assert enrich_orders(orders, customers) == [
        {"order_id": 1, "customer_id": "c1", "amount": 9.0, "region": "EU", "plan": "pro"},
        {"order_id": 2, "customer_id": "zz", "amount": 5.0, "region": None, "plan": None},
    ]


def test_inputs_unchanged():
    orders = [{"order_id": 1, "customer_id": "c1", "amount": 9.0}]
    customers = [{"customer_id": "c1", "region": "EU", "plan": "pro"}]
    o2, c2 = copy.deepcopy(orders), copy.deepcopy(customers)
    enrich_orders(orders, customers)
    assert orders == o2 and customers == c2


def test_duplicate_customer_last_wins():
    customers = [{"customer_id": "c1", "region": "EU", "plan": "free"},
                 {"customer_id": "c1", "region": "US", "plan": "pro"}]
    out = enrich_orders([{"order_id": 1, "customer_id": "c1", "amount": 1}], customers)
    assert out[0]["region"] == "US" and out[0]["plan"] == "pro"


def test_order_preserved_and_empty():
    orders = [{"order_id": i, "customer_id": "c", "amount": 0} for i in (3, 1, 2)]
    assert [r["order_id"] for r in enrich_orders(orders, [])] == [3, 1, 2]
    assert enrich_orders([], []) == []
