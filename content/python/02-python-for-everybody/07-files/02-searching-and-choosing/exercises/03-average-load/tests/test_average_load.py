from solution import average_load


def test_average(tmp_path):
    p = tmp_path / "m.txt"
    p.write_text("NOTE restarted\nLOAD 0.5\n\nLOAD 1.5\nLOADED 9\n", encoding="utf-8")
    assert average_load(p) == 1.0


def test_no_load_lines(tmp_path):
    p = tmp_path / "m.txt"
    p.write_text("NOTE a\nNOTE b\n", encoding="utf-8")
    assert average_load(p) is None


def test_single_without_newline(tmp_path):
    p = tmp_path / "m.txt"
    p.write_text("LOAD 2", encoding="utf-8")
    assert average_load(p) == 2.0


def test_empty(tmp_path):
    p = tmp_path / "m.txt"
    p.write_text("", encoding="utf-8")
    assert average_load(p) is None
