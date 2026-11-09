from solution import tidy_copy


def test_basic(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("  one  \n\n   \ntwo\n", encoding="utf-8")
    assert tidy_copy(a, b) == 2
    assert b.read_text(encoding="utf-8") == "one\ntwo\n"


def test_nothing_usable(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("\n  \n", encoding="utf-8")
    assert tidy_copy(a, b) == 0
    assert b.read_text(encoding="utf-8") == ""


def test_no_final_newline(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("x", encoding="utf-8")
    assert tidy_copy(a, b) == 1
    assert b.read_text(encoding="utf-8") == "x\n"


def test_source_untouched(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text(" y \n", encoding="utf-8")
    tidy_copy(a, b)
    assert a.read_text(encoding="utf-8") == " y \n"
