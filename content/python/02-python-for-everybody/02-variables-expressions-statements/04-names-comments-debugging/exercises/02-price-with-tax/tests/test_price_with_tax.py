from solution import total_with_tax


def test_basic():
    assert total_with_tax(80, 20) == 96.0


def test_zero_tax():
    assert total_with_tax(50, 0) == 50


def test_free_item():
    assert total_with_tax(0, 20) == 0


def test_small_tax():
    assert abs(total_with_tax(200, 5) - 210.0) < 1e-9
