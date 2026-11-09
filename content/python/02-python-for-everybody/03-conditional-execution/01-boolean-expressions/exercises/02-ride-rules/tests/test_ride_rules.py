from solution import may_ride


def test_both_ok():
    assert may_ride(130, 10) is True


def test_too_young():
    assert may_ride(130, 6) is False


def test_too_short():
    assert may_ride(110, 12) is False


def test_exactly_at_limits():
    assert may_ride(120, 8) is True
