from solution import get_order

ORDERS = {1001: {"order_id": 1001, "status": "shipped"}, 1002: {"order_id": 1002, "status": "refunded"}}


def test_found():
    assert get_order(ORDERS, "1001") == (200, {"order_id": 1001, "status": "shipped"})


def test_other_found():
    status, body = get_order(ORDERS, "1002")
    assert status == 200 and body["status"] == "refunded"


def test_missing_is_404_with_id():
    assert get_order(ORDERS, "7") == (404, {"error": "order 7 not found"})


def test_non_numeric_is_400():
    assert get_order(ORDERS, "abc") == (400, {"error": "invalid order id"})


def test_empty_is_400():
    assert get_order(ORDERS, "")[0] == 400


def test_does_not_mutate_store():
    before = dict(ORDERS)
    get_order(ORDERS, "9999")
    assert ORDERS == before
