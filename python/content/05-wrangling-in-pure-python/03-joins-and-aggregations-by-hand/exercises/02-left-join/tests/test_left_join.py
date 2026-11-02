import copy

from solution import left_join


def test_fan_out_and_unmatched():
    out = left_join(
        [{"id": 1}, {"id": 2}],
        [{"id": 1, "x": "a"}, {"id": 1, "x": "b"}],
        "id",
        ["x"],
    )
    assert out == [{"id": 1, "x": "a"}, {"id": 1, "x": "b"}, {"id": 2, "x": None}]


def test_left_order_and_extra_right_columns_ignored():
    left = [{"cid": 3, "n": "c"}, {"cid": 1, "n": "a"}]
    right = [{"cid": 1, "region": "EU", "junk": 0}, {"cid": 3, "region": "US", "junk": 1}]
    out = left_join(left, right, "cid", ["region"])
    assert out == [{"cid": 3, "n": "c", "region": "US"}, {"cid": 1, "n": "a", "region": "EU"}]


def test_inputs_not_modified():
    left = [{"id": 1}]
    right = [{"id": 1, "x": 1}]
    l0, r0 = copy.deepcopy(left), copy.deepcopy(right)
    left_join(left, right, "id", ["x"])
    assert left == l0 and right == r0


def test_empty_right_all_none():
    assert left_join([{"id": 1}], [], "id", ["x", "y"]) == [{"id": 1, "x": None, "y": None}]


def test_row_count_with_unique_right():
    left = [{"id": i} for i in range(5)]
    right = [{"id": i, "v": i} for i in range(3)]
    assert len(left_join(left, right, "id", ["v"])) == 5
