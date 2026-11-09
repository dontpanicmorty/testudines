from solution import at_least


def test_basic():
    assert at_least({"a": 5, "b": 1, "c": 3}, 3) == {"a": 5, "c": 3}


def test_boundary_included():
    assert at_least({"x": 2}, 2) == {"x": 2}


def test_none_pass():
    assert at_least({"x": 1}, 10) == {}


def test_empty():
    assert at_least({}, 0) == {}


def test_original_unchanged():
    d = {"a": 1, "b": 9}
    at_least(d, 5)
    assert d == {"a": 1, "b": 9}
