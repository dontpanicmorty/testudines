from solution import columns


def test_basic():
    assert columns({"b": 2, "a": 1, "c": 3}) == (["a", "b", "c"], [1, 2, 3])


def test_empty():
    assert columns({}) == ([], [])


def test_values_follow_keys():
    keys, values = columns({"z": "last", "m": "mid"})
    assert keys == ["m", "z"]
    assert values == ["mid", "last"]


def test_returns_tuple_of_lists():
    result = columns({"a": 1})
    assert isinstance(result, tuple)
    assert isinstance(result[0], list) and isinstance(result[1], list)


def test_original_unchanged():
    d = {"b": 1, "a": 2}
    columns(d)
    assert d == {"b": 1, "a": 2}
