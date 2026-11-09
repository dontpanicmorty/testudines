from solution import count_at_least


def test_basic():
    assert count_at_least([50, 70, 90, 70], 70) == 3


def test_none_qualify():
    assert count_at_least([1, 2], 10) == 0


def test_empty():
    assert count_at_least([], 5) == 0


def test_negative_numbers():
    assert count_at_least([-5, -1, -9], -5) == 2
