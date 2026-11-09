from solution import index_paid, line_numbers


def test_index_paid():
    orders = [{"order_id": "a", "status": "Paid ", "amount": 5.0},
              {"order_id": "b", "status": "refunded", "amount": 9.0},
              {"order_id": "a", "status": "paid", "amount": 7.0}]
    assert index_paid(orders) == {"a": 7.0}


def test_index_paid_empty():
    assert index_paid([]) == {}


def test_line_numbers():
    assert line_numbers(["x", "y"]) == ["1: x", "2: y"]
    assert line_numbers([]) == []
