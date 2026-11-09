from decimal import Decimal

from solution import invoice_total


def test_exact_small_sums():
    assert invoice_total([(3, "0.10")], "0") == Decimal("0.30")
    assert invoice_total([(10, "0.10")], "0") == Decimal("1.00")


def test_half_up():
    assert invoice_total([(1, "2.675")], "0") == Decimal("2.68")


def test_with_tax():
    assert invoice_total([(2, "19.99"), (1, "5.00")], "0.0825") == Decimal("48.69")


def test_type_and_places():
    out = invoice_total([(1, "1.00")], "0")
    assert isinstance(out, Decimal)
    assert str(out) == "1.00"


def test_empty():
    assert invoice_total([], "0.1") == Decimal("0.00")
