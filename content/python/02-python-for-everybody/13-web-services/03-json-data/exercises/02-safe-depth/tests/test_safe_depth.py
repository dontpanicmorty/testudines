from solution import dig

TEXT = '{"a": {"b": [10, 20, {"c": "deep"}]}, "n": 5, "z": null}'


def test_deep():
    assert dig(TEXT, ["a", "b", 2, "c"]) == "deep"


def test_missing_key():
    assert dig(TEXT, ["a", "x"], "none") == "none"


def test_index_out_of_range():
    assert dig(TEXT, ["a", "b", 9], -1) == -1


def test_into_a_number():
    assert dig(TEXT, ["n", "oops"], "bad") == "bad"


def test_null_value_is_returned():
    assert dig(TEXT, ["z"], "dflt") is None


def test_empty_path_returns_everything():
    assert dig('[1, 2]', []) == [1, 2]
