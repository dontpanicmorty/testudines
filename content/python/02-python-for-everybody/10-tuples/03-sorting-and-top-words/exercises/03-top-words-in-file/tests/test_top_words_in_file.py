from solution import favourites


def write(tmp_path, text):
    p = tmp_path / "t.txt"
    p.write_text(text, encoding="utf-8")
    return p


def test_basic(tmp_path):
    p = write(tmp_path, "The rain, the RAIN!\nThe sun. A sun.\n")
    assert favourites(p, 2) == [("the", 3), ("rain", 2)]


def test_ties_alphabetical(tmp_path):
    p = write(tmp_path, "b a c\n")
    assert favourites(p, 2) == [("a", 1), ("b", 1)]


def test_fewer_words_than_n(tmp_path):
    p = write(tmp_path, "hello hello\n")
    assert favourites(p, 5) == [("hello", 2)]


def test_empty_file(tmp_path):
    assert favourites(write(tmp_path, ""), 3) == []


def test_punctuation_only_ignored(tmp_path):
    p = write(tmp_path, "-- !! a\n")
    assert favourites(p, 3) == [("a", 1)]
