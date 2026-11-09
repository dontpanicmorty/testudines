from solution import body_index


def test_typical():
    assert abs(body_index(70, 175) - 22.857142857) < 1e-6


def test_taller():
    assert abs(body_index(90, 200) - 22.5) < 1e-9


def test_metre_tall():
    assert body_index(50, 100) == 50


def test_zero_weight():
    assert body_index(0, 170) == 0
