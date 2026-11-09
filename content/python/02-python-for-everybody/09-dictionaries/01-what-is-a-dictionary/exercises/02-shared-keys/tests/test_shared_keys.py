from solution import in_both


def test_overlap():
    a = {"Ana": 1, "Ben": 2, "Cy": 3}
    b = {"Cy": 9, "Ana": 8, "Dee": 7}
    assert in_both(a, b) == ["Ana", "Cy"]


def test_no_overlap():
    assert in_both({"a": 1}, {"b": 2}) == []


def test_empty():
    assert in_both({}, {"b": 2}) == []
    assert in_both({"b": 2}, {}) == []


def test_sorted_output():
    a = {"zed": 1, "amy": 1, "mo": 1}
    assert in_both(a, dict(a)) == ["amy", "mo", "zed"]


def test_values_ignored():
    assert in_both({"x": 1}, {"x": 99}) == ["x"]
