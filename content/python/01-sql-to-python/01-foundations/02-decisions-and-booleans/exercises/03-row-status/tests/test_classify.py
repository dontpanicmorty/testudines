import pytest
from solution import classify_order


@pytest.mark.parametrize("row,expected", [
    (None, "invalid"),
    ({}, "invalid"),
    ({"status": 3, "amount": 5}, "invalid"),
    ({"status": None, "amount": 5}, "invalid"),
    ({"status": "Cancelled", "amount": 5}, "closed"),
    ({"status": " RETURNED", "amount": None}, "closed"),
    ({"status": "shipped"}, "unpaid"),
    ({"status": "pending", "amount": 0}, "unpaid"),
    ({"status": "pending", "amount": None}, "unpaid"),
    ({"status": "Shipped ", "amount": 50}, "fulfilled"),
    ({"status": "delivered", "amount": 1}, "fulfilled"),
    ({"status": "pending", "amount": 50}, "open"),
])
def test_classify(row, expected):
    assert classify_order(row) == expected, f"classify_order({row!r})"
