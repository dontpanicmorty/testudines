from solution import change_due


def test_normal():
    assert change_due(350, 500) == 150


def test_exact():
    assert change_due(999, 999) == 0


def test_large():
    assert change_due(1, 10000) == 9999


def test_short_payment_is_negative():
    assert change_due(500, 450) == -50
