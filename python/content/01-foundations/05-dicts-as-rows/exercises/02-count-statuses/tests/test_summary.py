from solution import summarise


def test_basic():
    orders = [
        {"status": "paid", "amount": 10.5},
        {"status": "paid", "amount": 4.25},
        {"status": "refunded", "amount": 3.0},
    ]
    assert summarise(orders) == {
        "paid": {"count": 2, "total": 14.75},
        "refunded": {"count": 1, "total": 3.0},
    }


def test_empty():
    assert summarise([]) == {}


def test_float_noise_rounded():
    orders = [{"status": "a", "amount": 0.1}, {"status": "a", "amount": 0.2}]
    assert summarise(orders) == {"a": {"count": 2, "total": 0.3}}
