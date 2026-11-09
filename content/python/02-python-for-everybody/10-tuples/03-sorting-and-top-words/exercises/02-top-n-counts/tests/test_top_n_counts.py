from solution import top_n


def test_basic():
    counts = {"tea": 3, "milk": 5, "rice": 3, "oat": 1}
    assert top_n(counts, 3) == [("milk", 5), ("rice", 3), ("tea", 3)]


def test_n_larger_than_size():
    assert top_n({"a": 1}, 10) == [("a", 1)]


def test_zero():
    assert top_n({"a": 1}, 0) == []


def test_empty():
    assert top_n({}, 3) == []


def test_all_ties():
    assert top_n({"c": 2, "a": 2, "b": 2}, 2) == [("a", 2), ("b", 2)]
