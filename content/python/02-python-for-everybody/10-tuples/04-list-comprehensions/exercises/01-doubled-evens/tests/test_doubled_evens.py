from solution import double_evens


def test_basic():
    assert double_evens([1, 2, 3, 4]) == [4, 8]


def test_empty():
    assert double_evens([]) == []


def test_no_evens():
    assert double_evens([1, 3, 5]) == []


def test_negative_and_zero():
    assert double_evens([-2, 0, -3]) == [-4, 0]


def test_input_unchanged():
    data = [2, 4]
    double_evens(data)
    assert data == [2, 4]
