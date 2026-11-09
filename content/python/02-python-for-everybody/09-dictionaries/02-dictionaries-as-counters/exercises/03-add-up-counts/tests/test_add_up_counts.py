from solution import combine


def test_overlap():
    assert combine({"fig": 2, "pear": 1}, {"pear": 4, "plum": 5}) == {"fig": 2, "pear": 5, "plum": 5}


def test_both_empty():
    assert combine({}, {}) == {}


def test_one_empty():
    assert combine({"a": 1}, {}) == {"a": 1}
    assert combine({}, {"a": 1}) == {"a": 1}


def test_inputs_not_changed():
    a = {"x": 1}
    b = {"x": 2, "y": 3}
    result = combine(a, b)
    assert a == {"x": 1}
    assert b == {"x": 2, "y": 3}
    assert result == {"x": 3, "y": 3}


def test_returns_new_object():
    a = {"x": 1}
    assert combine(a, {}) is not a
