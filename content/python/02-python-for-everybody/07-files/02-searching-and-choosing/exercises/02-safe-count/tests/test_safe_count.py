from solution import count_word_lines


def test_counts(tmp_path):
    p = tmp_path / "n.txt"
    p.write_text("red car\nblue car\nred bike\n", encoding="utf-8")
    assert count_word_lines(p, "car") == 2


def test_missing_file(tmp_path):
    assert count_word_lines(tmp_path / "nothing.txt", "x") is None


def test_exists_but_zero(tmp_path):
    p = tmp_path / "n.txt"
    p.write_text("hello\n", encoding="utf-8")
    assert count_word_lines(p, "zebra") == 0


def test_empty_file_is_zero_not_none(tmp_path):
    p = tmp_path / "n.txt"
    p.write_text("", encoding="utf-8")
    assert count_word_lines(p, "a") == 0
