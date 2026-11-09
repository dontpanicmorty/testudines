from solution import shop_price


def test_with_discount():
    assert abs(shop_price(100, 10) - 108.0) < 1e-9


def test_no_discount():
    assert abs(shop_price(50, 0) - 60.0) < 1e-9


def test_full_discount():
    assert shop_price(80, 100) == 0


def test_free_item():
    assert shop_price(0, 25) == 0
