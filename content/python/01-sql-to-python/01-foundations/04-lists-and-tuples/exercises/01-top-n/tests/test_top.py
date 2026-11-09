from solution import top_n


def test_basic():
    orders = [("o1", 50), ("o2", 90), ("o3", 20)]
    assert top_n(orders, 2) == [("o2", 90), ("o1", 50)]


def test_n_larger_than_list():
    assert top_n([("a", 1), ("b", 2)], 10) == [("b", 2), ("a", 1)]


def test_ties_stable():
    assert top_n([("a", 5), ("b", 5), ("c", 1)], 2) == [("a", 5), ("b", 5)]


def test_input_unchanged():
    orders = [("o1", 50), ("o2", 90)]
    top_n(orders, 1)
    assert orders == [("o1", 50), ("o2", 90)]


def test_zero_and_empty():
    assert top_n([], 3) == []
    assert top_n([("a", 1)], 0) == []
