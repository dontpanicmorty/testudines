from solution import sum_stepped


def test_positive_step():
    assert sum_stepped(1, 10, 3) == 12


def test_negative_step():
    assert sum_stepped(5, 0, -2) == 9


def test_nothing_in_range():
    assert sum_stepped(5, 5, 1) == 0


def test_wrong_direction():
    assert sum_stepped(1, 10, -1) == 0
