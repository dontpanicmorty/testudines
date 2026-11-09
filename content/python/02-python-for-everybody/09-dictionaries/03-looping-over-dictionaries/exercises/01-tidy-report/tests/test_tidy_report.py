from solution import report


def test_sorted_by_name():
    assert report({"pears": 4, "apples": 12}) == ["apples: 12", "pears: 4"]


def test_empty():
    assert report({}) == []


def test_zero_count_kept():
    assert report({"plums": 0}) == ["plums: 0"]


def test_single():
    assert report({"x": 1}) == ["x: 1"]


def test_many():
    stock = {"c": 3, "a": 1, "b": 2}
    assert report(stock) == ["a: 1", "b: 2", "c: 3"]
