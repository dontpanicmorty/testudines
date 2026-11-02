from solution import check_orders


def test_clean():
    assert check_orders([{"order_id": 1, "amount": 5}, {"order_id": 2, "amount": 0}]) == []


def test_empty():
    assert check_orders([]) == ["empty"]


def test_null_ids_not_counted_as_duplicates():
    rows = [{"order_id": None, "amount": 1}, {"order_id": None, "amount": 2}]
    assert check_orders(rows) == ["null_order_id"]


def test_missing_id_key():
    assert check_orders([{"amount": 1}]) == ["null_order_id"]


def test_duplicates_and_bad_amount_order():
    rows = [{"order_id": 1, "amount": 5.0}, {"order_id": 1, "amount": -1}]
    assert check_orders(rows) == ["duplicate_order_id", "bad_amount"]


def test_bad_amount_variants_reported_once():
    rows = [
        {"order_id": 1, "amount": None},
        {"order_id": 2},
        {"order_id": 3, "amount": "12"},
        {"order_id": 4, "amount": -3},
    ]
    assert check_orders(rows) == ["bad_amount"]


def test_everything_wrong():
    rows = [{"order_id": None, "amount": 1}, {"order_id": 2, "amount": 1},
            {"order_id": 2, "amount": "x"}]
    assert check_orders(rows) == ["null_order_id", "duplicate_order_id", "bad_amount"]
