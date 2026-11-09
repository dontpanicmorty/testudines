from solution import lowest


def test_mixed():
    assert lowest([4, -2, 9]) == -2


def test_all_negative():
    assert lowest([-3, -8, -5]) == -8


def test_empty_is_none():
    assert lowest([]) is None


def test_single():
    assert lowest([7]) == 7
