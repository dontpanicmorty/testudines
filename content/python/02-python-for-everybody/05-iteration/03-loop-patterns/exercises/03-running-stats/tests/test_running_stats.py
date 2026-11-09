from solution import summarize


def test_basic():
    assert summarize([3, 9, 4]) == {"count": 3, "total": 16, "largest": 9}


def test_empty():
    assert summarize([]) == {"count": 0, "total": 0, "largest": None}


def test_negatives():
    assert summarize([-4, -2]) == {"count": 2, "total": -6, "largest": -2}


def test_single_zero():
    assert summarize([0]) == {"count": 1, "total": 0, "largest": 0}
