import pytest

from solution import assert_matches_golden


def test_update_writes_file_and_creates_folders(tmp_path):
    path = tmp_path / "deep" / "er" / "report.txt"
    assert assert_matches_golden("EU 17\nUS 5\n", path, update=True) is None
    assert path.read_text() == "EU 17\nUS 5\n"


def test_match_passes(tmp_path):
    path = tmp_path / "g.txt"
    path.write_text("a\nb\n")
    assert assert_matches_golden("a\nb\n", path) is None


def test_accepts_str_path(tmp_path):
    path = tmp_path / "g.txt"
    path.write_text("x\n")
    assert_matches_golden("x\n", str(path))


def test_mismatch_raises_with_diff(tmp_path):
    path = tmp_path / "g.txt"
    path.write_text("EU 17\nUS 5\n")
    with pytest.raises(AssertionError) as info:
        assert_matches_golden("EU 18\nUS 5\n", path)
    msg = str(info.value)
    assert "-EU 17" in msg, msg
    assert "+EU 18" in msg, msg


def test_mismatch_does_not_overwrite(tmp_path):
    path = tmp_path / "g.txt"
    path.write_text("old\n")
    with pytest.raises(AssertionError):
        assert_matches_golden("new\n", path)
    assert path.read_text() == "old\n"


def test_missing_golden_fails_and_mentions_update(tmp_path):
    path = tmp_path / "nope.txt"
    with pytest.raises(AssertionError, match="update=True"):
        assert_matches_golden("x\n", path)
    assert not path.exists()


def test_update_overwrites_existing(tmp_path):
    path = tmp_path / "g.txt"
    path.write_text("old\n")
    assert_matches_golden("new\n", path, update=True)
    assert path.read_text() == "new\n"


def test_trailing_newline_difference_is_a_mismatch(tmp_path):
    path = tmp_path / "g.txt"
    path.write_text("a\n")
    with pytest.raises(AssertionError):
        assert_matches_golden("a", path)
