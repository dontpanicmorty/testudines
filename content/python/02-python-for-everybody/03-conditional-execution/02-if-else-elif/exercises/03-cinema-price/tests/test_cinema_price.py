from solution import ticket_price


def test_adult():
    assert ticket_price(30, False) == 10
    assert ticket_price(30, True) == 8


def test_child_no_discount():
    assert ticket_price(8, False) == 5
    assert ticket_price(8, True) == 5


def test_senior():
    assert ticket_price(70, False) == 6
    assert ticket_price(70, True) == 4


def test_age_boundaries():
    assert ticket_price(11, False) == 5
    assert ticket_price(12, False) == 10
    assert ticket_price(64, False) == 10
    assert ticket_price(65, False) == 6
