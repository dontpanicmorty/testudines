from pathlib import Path

from solution import write_daily_report


def test_creates_nested_dirs_and_content(tmp_path):
    p = write_daily_report(tmp_path / "out" / "reports", "2025-06-01", ["ok: 10", "failed: 2"])
    assert isinstance(p, Path)
    assert p.name == "2025-06-01.txt"
    assert p.read_text(encoding="utf-8") == "ok: 10\nfailed: 2\n"


def test_idempotent(tmp_path):
    write_daily_report(tmp_path, "d", ["a", "b"])
    p = write_daily_report(tmp_path, "d", ["a", "b"])
    assert p.read_text(encoding="utf-8") == "a\nb\n", "second call must replace, not append"


def test_unicode(tmp_path):
    p = write_daily_report(tmp_path, "d", ["Zoë"])
    # UTF-8 bytes; Windows writes "\r\n" line endings in text mode, which is fine
    assert p.read_bytes().replace(b"\r\n", b"\n") == "Zoë\n".encode("utf-8")
