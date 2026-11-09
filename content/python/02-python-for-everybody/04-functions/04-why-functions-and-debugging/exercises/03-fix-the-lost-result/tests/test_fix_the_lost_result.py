from solution import add_delivery, add_tax, final_total


def test_final_total():
    assert abs(final_total(100, 20, 5) - 125.0) < 1e-9


def test_no_tax():
    assert final_total(40, 0, 3) == 43


def test_add_tax_returns_a_value():
    assert abs(add_tax(50, 10) - 55.0) < 1e-9


def test_add_delivery():
    assert add_delivery(10, 4) == 14


def test_free_delivery():
    assert abs(final_total(10, 50, 0) - 15.0) < 1e-9
