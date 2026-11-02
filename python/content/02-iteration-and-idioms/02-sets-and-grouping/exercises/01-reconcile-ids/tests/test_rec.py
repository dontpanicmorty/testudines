from solution import reconcile


def test_basic():
    assert reconcile([1, 2, 3, 3], [2, 3, 4]) == {"missing": [1], "unexpected": [4], "matched": [2, 3]}


def test_empty():
    assert reconcile([], []) == {"missing": [], "unexpected": [], "matched": []}
    assert reconcile(["a"], []) == {"missing": ["a"], "unexpected": [], "matched": []}


def test_identical():
    assert reconcile([3, 1], [1, 3, 1]) == {"missing": [], "unexpected": [], "matched": [1, 3]}
