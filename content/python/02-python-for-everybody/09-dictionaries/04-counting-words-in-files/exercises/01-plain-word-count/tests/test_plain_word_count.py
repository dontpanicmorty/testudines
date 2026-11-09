from solution import count_words


def test_basic(tmp_path):
    p = tmp_path / "t.txt"
    p.write_text("to be\nor not to be\n", encoding="utf-8")
    assert count_words(p) == {"to": 2, "be": 2, "or": 1, "not": 1}


def test_empty_file(tmp_path):
    p = tmp_path / "t.txt"
    p.write_text("", encoding="utf-8")
    assert count_words(p) == {}


def test_case_and_punctuation_untouched(tmp_path):
    p = tmp_path / "t.txt"
    p.write_text("Hi hi, hi\n", encoding="utf-8")
    assert count_words(p) == {"Hi": 1, "hi": 1, "hi,": 1}


def test_blank_lines_and_extra_spaces(tmp_path):
    p = tmp_path / "t.txt"
    p.write_text("a   a\n\n\t a\n", encoding="utf-8")
    assert count_words(p) == {"a": 3}
