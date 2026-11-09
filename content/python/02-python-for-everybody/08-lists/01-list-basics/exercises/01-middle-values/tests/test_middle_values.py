from solution import without_ends


def test_basic():
    assert without_ends([1, 2, 3, 4]) == [2, 3]


def test_short():
    assert without_ends([1, 2]) == []
    assert without_ends([1]) == []


def test_empty():
    assert without_ends([]) == []


def test_original_kept():
    data = [1, 2, 3]
    without_ends(data)
    assert data == [1, 2, 3]
