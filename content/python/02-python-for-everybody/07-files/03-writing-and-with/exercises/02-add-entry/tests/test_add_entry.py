from solution import add_entry


def test_creates_file(tmp_path):
    p = tmp_path / "d.txt"
    add_entry(p, "Mon", "rain")
    assert p.read_text(encoding="utf-8") == "Mon: rain\n"


def test_keeps_earlier(tmp_path):
    p = tmp_path / "d.txt"
    p.write_text("Sun: sun\n", encoding="utf-8")
    add_entry(p, "Mon", "rain")
    assert p.read_text(encoding="utf-8") == "Sun: sun\nMon: rain\n"


def test_two_calls(tmp_path):
    p = tmp_path / "d.txt"
    add_entry(p, "A", "1")
    add_entry(p, "B", "2")
    assert p.read_text(encoding="utf-8") == "A: 1\nB: 2\n"
