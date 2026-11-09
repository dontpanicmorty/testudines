from solution import excited


def test_basic():
    assert excited(["hi", "ok"]) == ["hi!", "ok!"]


def test_empty():
    assert excited([]) == []


def test_original_unchanged():
    words = ["a"]
    excited(words)
    assert words == ["a"]


def test_empty_string_entry():
    assert excited([""]) == ["!"]
