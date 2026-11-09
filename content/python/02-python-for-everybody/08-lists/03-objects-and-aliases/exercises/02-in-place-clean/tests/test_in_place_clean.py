from solution import uppercase_all


def test_changes_caller_list():
    w = ["a", "Bc"]
    uppercase_all(w)
    assert w == ["A", "BC"]


def test_returns_none():
    assert uppercase_all(["x"]) is None


def test_same_object_kept():
    w = ["q"]
    alias = w
    uppercase_all(w)
    assert alias == ["Q"]


def test_empty():
    w = []
    uppercase_all(w)
    assert w == []
