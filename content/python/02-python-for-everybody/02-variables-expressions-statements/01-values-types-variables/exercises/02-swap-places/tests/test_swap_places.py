from solution import swap


def test_text():
    assert swap("tea", "coffee") == ("coffee", "tea")


def test_numbers():
    assert swap(1, 2) == (2, 1)


def test_mixed_types():
    assert swap(1, "one") == ("one", 1)


def test_same_values():
    assert swap(5, 5) == (5, 5)
