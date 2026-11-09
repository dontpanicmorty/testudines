from solution import quoted


def test_two_phrases():
    assert quoted('He said "red" and "blue".') == ["red", "blue"]


def test_no_quotes():
    assert quoted("plain text") == []


def test_empty_quotes():
    assert quoted('a "" b') == [""]


def test_spaces_inside_kept():
    assert quoted('say "hello there" now') == ["hello there"]


def test_three_phrases_not_merged():
    assert quoted('"a" x "b" y "c"') == ["a", "b", "c"]


def test_unclosed_quote_ignored():
    assert quoted('"done" and "open') == ["done"]
