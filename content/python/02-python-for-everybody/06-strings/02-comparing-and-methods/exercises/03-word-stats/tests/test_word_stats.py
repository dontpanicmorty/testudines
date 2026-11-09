from solution import longest_word


def test_tie_goes_to_first():
    assert longest_word("the quick brown fox") == "quick"


def test_extra_spaces():
    assert longest_word("  a   bbb  cc ") == "bbb"


def test_empty():
    assert longest_word("") == ""


def test_one_word():
    assert longest_word("solo") == "solo"
