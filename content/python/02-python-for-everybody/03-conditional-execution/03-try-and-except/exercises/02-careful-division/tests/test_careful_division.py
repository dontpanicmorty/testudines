from solution import safe_share


def test_normal():
    assert safe_share(10, 4) == 2.5


def test_zero_people():
    assert safe_share(10, 0) is None


def test_zero_total():
    assert safe_share(0, 5) == 0


def test_negative_total():
    assert safe_share(-9, 3) == -3
