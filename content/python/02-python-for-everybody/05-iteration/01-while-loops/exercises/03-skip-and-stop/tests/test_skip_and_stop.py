from solution import collect_words


def test_basic():
    assert collect_words(["a", "", "b", "STOP", "c"]) == ["a", "b"]


def test_no_stop_word():
    assert collect_words(["x", "y"]) == ["x", "y"]


def test_empty_list():
    assert collect_words([]) == []


def test_stop_first():
    assert collect_words(["STOP", "a"]) == []


def test_only_blanks():
    assert collect_words(["", "", ""]) == []
