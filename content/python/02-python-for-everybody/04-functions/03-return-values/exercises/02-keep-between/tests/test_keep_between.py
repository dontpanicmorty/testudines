from solution import limit


def test_too_high():
    assert limit(15, 0, 10) == 10


def test_too_low():
    assert limit(-3, 0, 10) == 0


def test_inside():
    assert limit(4, 0, 10) == 4


def test_on_the_limits():
    assert limit(0, 0, 10) == 0
    assert limit(10, 0, 10) == 10


def test_decimals():
    assert limit(0.5, 1.0, 2.0) == 1.0
