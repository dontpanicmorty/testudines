from solution import rectangle_facts


def test_basic():
    assert rectangle_facts(5, 3) == (15, 16)


def test_square():
    assert rectangle_facts(4, 4) == (16, 16)


def test_decimals():
    assert rectangle_facts(2.5, 2) == (5.0, 9.0)


def test_zero_width():
    assert rectangle_facts(7, 0) == (0, 14)
