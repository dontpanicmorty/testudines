import copy

from solution import dedupe, keep_first, keep_last, keep_max

ROWS = [
    {"id": 2, "v": 9, "t": "a"},
    {"id": 1, "v": 3, "t": "b"},
    {"id": 1, "v": 7, "t": "c"},
    {"id": 2, "v": 9, "t": "d"},
    {"id": 3, "v": 1, "t": "e"},
    {"id": 1, "v": 7, "t": "f"},
]


def ts(rows):
    return [r["t"] for r in rows]


def test_keep_first():
    assert ts(dedupe(ROWS, "id", keep_first)) == ["a", "b", "e"]


def test_keep_last():
    assert ts(dedupe(ROWS, "id", keep_last)) == ["d", "f", "e"]


def test_keep_max_with_first_wins_on_ties():
    assert ts(dedupe(ROWS, "id", keep_max("v"))) == ["a", "c", "e"]


def test_order_is_first_appearance_of_key():
    assert [r["id"] for r in dedupe(ROWS, "id", keep_last)] == [2, 1, 3]


def test_input_not_modified():
    before = copy.deepcopy(ROWS)
    dedupe(ROWS, "id", keep_first)
    assert ROWS == before


def test_custom_strategy_is_accepted():
    shortest = lambda group: min(group, key=lambda r: r["t"])  # noqa: E731
    assert ts(dedupe(ROWS, "id", shortest)) == ["a", "b", "e"]


def test_strategies_are_plain_functions():
    assert callable(keep_max("v"))
    assert keep_first([{"x": 1}, {"x": 2}]) == {"x": 1}
    assert keep_last([{"x": 1}, {"x": 2}]) == {"x": 2}


def test_empty():
    assert dedupe([], "id", keep_first) == []
