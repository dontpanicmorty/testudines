from solution import tally


def test_basic():
    assert tally(["kiwi", "plum", "kiwi"]) == {"kiwi": 2, "plum": 1}


def test_empty():
    assert tally([]) == {}


def test_single_item_repeated():
    assert tally(["a"] * 5) == {"a": 5}


def test_case_sensitive():
    assert tally(["A", "a"]) == {"A": 1, "a": 1}


def test_counts_add_up():
    votes = list("mississippi")
    assert sum(tally(votes).values()) == len(votes)
