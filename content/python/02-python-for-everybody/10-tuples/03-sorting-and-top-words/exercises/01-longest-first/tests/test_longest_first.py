from solution import longest_first


def test_basic():
    words = ["fig", "banana", "kiwi", "pear", "apple"]
    assert longest_first(words) == ["banana", "apple", "kiwi", "pear", "fig"]


def test_empty():
    assert longest_first([]) == []


def test_ties_alphabetical():
    assert longest_first(["bb", "aa", "cc"]) == ["aa", "bb", "cc"]


def test_input_unchanged():
    words = ["b", "aa"]
    longest_first(words)
    assert words == ["b", "aa"]


def test_duplicates_kept():
    assert longest_first(["a", "a"]) == ["a", "a"]
