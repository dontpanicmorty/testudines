from solution import flip


def test_basic():
    assert flip([("a", 1), ("b", 2)]) == [(1, "a"), (2, "b")]


def test_empty():
    assert flip([]) == []


def test_equal_items():
    assert flip([(3, 3)]) == [(3, 3)]


def test_results_are_tuples():
    assert all(isinstance(p, tuple) for p in flip([(1, 2), (3, 4)]))


def test_input_unchanged():
    data = [("x", "y")]
    flip(data)
    assert data == [("x", "y")]
