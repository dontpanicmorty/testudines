from solution import doubled


def test_basic():
    assert doubled([1, 2, 3]) == [2, 4, 6]


def test_original_unchanged():
    data = [5, 6]
    doubled(data)
    assert data == [5, 6]


def test_returns_new_list():
    data = [1]
    assert doubled(data) is not data


def test_empty():
    assert doubled([]) == []
