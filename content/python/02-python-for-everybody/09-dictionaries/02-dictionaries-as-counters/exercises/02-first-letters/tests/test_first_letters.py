from solution import starting_letters


def test_basic():
    assert starting_letters(["Apple", "avocado", "Banana", ""]) == {"a": 2, "b": 1}


def test_all_empty():
    assert starting_letters(["", ""]) == {}


def test_no_words():
    assert starting_letters([]) == {}


def test_case_folded():
    assert starting_letters(["Zed", "zebra", "ZIP"]) == {"z": 3}


def test_keys_are_single_lowercase_letters():
    result = starting_letters(["Tea", "coffee", "Cocoa"])
    assert result == {"t": 1, "c": 2}
