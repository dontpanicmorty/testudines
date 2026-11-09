import dataclasses

import pytest

from solution import OrderLine


def test_normalises_sku():
    assert OrderLine(7, " ab-12 ", 3, 250).sku == "AB-12"


def test_total():
    assert OrderLine(1, "x", 3, 250).total_cents == 750
    assert OrderLine(1, "x", 1, 0).total_cents == 0


def test_blank_sku_rejected():
    with pytest.raises(ValueError, match="sku"):
        OrderLine(1, "   ", 1, 100)


@pytest.mark.parametrize("qty", [0, -1])
def test_bad_quantity(qty):
    with pytest.raises(ValueError, match="quantity"):
        OrderLine(1, "x", qty, 100)


def test_negative_price():
    with pytest.raises(ValueError, match="unit_price_cents"):
        OrderLine(1, "x", 1, -1)


def test_frozen():
    line = OrderLine(1, "x", 1, 100)
    with pytest.raises(dataclasses.FrozenInstanceError):
        line.quantity = 5


def test_hashable_and_equal():
    a = OrderLine(1, "x", 1, 100)
    b = OrderLine(1, " X ", 1, 100)
    assert a == b
    assert len({a, b}) == 1
