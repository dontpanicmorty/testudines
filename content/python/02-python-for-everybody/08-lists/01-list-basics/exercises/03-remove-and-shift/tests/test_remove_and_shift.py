from solution import drop_all


def test_basic():
    items = [1, 2, 2, 3, 2]
    assert drop_all(items, 2) == 3
    assert items == [1, 3]


def test_neighbours():
    items = ["x", "x", "x", "y"]
    assert drop_all(items, "x") == 3
    assert items == ["y"]


def test_absent():
    items = [1, 2]
    assert drop_all(items, 9) == 0
    assert items == [1, 2]


def test_empty():
    items = []
    assert drop_all(items, 1) == 0
    assert items == []
