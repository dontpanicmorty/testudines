from solution import swap_ends


def test_basic():
    assert swap_ends("hello") == "oellh"


def test_two_characters():
    assert swap_ends("ab") == "ba"


def test_short_strings():
    assert swap_ends("") == ""
    assert swap_ends("q") == "q"


def test_same_ends():
    assert swap_ends("abca") == "abca"
