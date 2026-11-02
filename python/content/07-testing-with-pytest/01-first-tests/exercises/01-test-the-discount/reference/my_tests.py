import pytest

from pricing import apply_discount


def test_typical():
    assert apply_discount(200, 25) == 150.0


def test_zero_percent_changes_nothing():
    assert apply_discount(50, 0) == 50


def test_hundred_percent_is_free():
    assert apply_discount(50, 100) == 0


def test_rounds_to_two_decimals():
    assert apply_discount(10, 33.33) == 6.67


def test_negative_percent_rejected():
    with pytest.raises(ValueError):
        apply_discount(10, -1)


def test_over_hundred_rejected():
    with pytest.raises(ValueError):
        apply_discount(10, 101)
