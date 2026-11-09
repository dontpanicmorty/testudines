from solution import lines_with_prefix

LOG = "INFO start\nWARN disk 91%\nINFO user ana joined\nERROR db timeout\n\nWARN retrying\n"


def test_warnings(tmp_path):
    p = tmp_path / "s.log"
    p.write_text(LOG, encoding="utf-8")
    assert lines_with_prefix(p, "WARN") == ["WARN disk 91%", "WARN retrying"]


def test_no_match(tmp_path):
    p = tmp_path / "s.log"
    p.write_text(LOG, encoding="utf-8")
    assert lines_with_prefix(p, "DEBUG") == []


def test_case_sensitive(tmp_path):
    p = tmp_path / "s.log"
    p.write_text(LOG, encoding="utf-8")
    assert lines_with_prefix(p, "warn") == []


def test_empty_prefix_matches_all(tmp_path):
    p = tmp_path / "s.log"
    p.write_text("a\nb\n", encoding="utf-8")
    assert lines_with_prefix(p, "") == ["a", "b"]
