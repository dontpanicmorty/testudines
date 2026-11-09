from solution import tag_batch


def test_basic():
    assert tag_batch([{"id": 1}], ["eu"]) == [{"id": 1, "tags": ["eu", "loaded"]}]


def test_calls_independent():
    tag_batch([{"id": 1}], ["eu"])
    assert tag_batch([{"id": 2}]) == [{"id": 2, "tags": ["loaded"]}]
    assert tag_batch([{"id": 3}]) == [{"id": 3, "tags": ["loaded"]}]


def test_input_rows_not_mutated():
    rows = [{"id": 1}]
    tag_batch(rows, ["x"])
    assert rows == [{"id": 1}], "the caller's rows were modified"


def test_input_tags_not_mutated():
    tags = ["eu"]
    tag_batch([{"id": 1}], tags)
    assert tags == ["eu"], "the caller's tags list was modified"


def test_rows_do_not_share_tag_list():
    out = tag_batch([{"id": 1}, {"id": 2}])
    out[0]["tags"].append("x")
    assert out[1]["tags"] == ["loaded"]
