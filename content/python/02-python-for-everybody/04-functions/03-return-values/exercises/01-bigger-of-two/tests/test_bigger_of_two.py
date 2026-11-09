from solution import larger


def test_second_bigger():
    assert larger(3, 9) == 9


def test_first_bigger():
    assert larger(10, 2) == 10


def test_negatives():
    assert larger(-1, -5) == -1


def test_equal():
    assert larger(4, 4) == 4
