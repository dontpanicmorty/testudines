import pytest
from solution import order_tier


@pytest.mark.parametrize("amount,expected", [
    (2500, "enterprise"), (1000, "enterprise"), (999.99, "standard"),
    (100, "standard"), (99, "small"), (0.5, "small"), (0, "none"), (-3, "none"),
])
def test_tier(amount, expected):
    assert order_tier(amount) == expected, f"order_tier({amount})"
