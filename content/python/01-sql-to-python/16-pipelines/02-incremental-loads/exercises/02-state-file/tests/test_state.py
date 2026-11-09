import json

import pytest

from solution import load_state, save_state


def test_missing_file_gives_default(tmp_path):
    assert load_state(tmp_path / "nope.json") == {"watermark": None}


def test_roundtrip(tmp_path):
    p = tmp_path / "s.json"
    save_state(p, {"watermark": "2026-01-02T00:00:00", "rows": 5})
    assert load_state(p) == {"watermark": "2026-01-02T00:00:00", "rows": 5}


def test_creates_parent_dir(tmp_path):
    p = tmp_path / "state" / "deep" / "orders.json"
    save_state(p, {"watermark": "x"})
    assert json.loads(p.read_text()) == {"watermark": "x"}


def test_no_temp_files_left(tmp_path):
    p = tmp_path / "s.json"
    save_state(p, {"watermark": "a"})
    save_state(p, {"watermark": "b"})
    assert [f.name for f in tmp_path.iterdir()] == ["s.json"]


def test_old_file_without_watermark_key(tmp_path):
    p = tmp_path / "s.json"
    p.write_text(json.dumps({"rows": 3}))
    assert load_state(p) == {"watermark": None, "rows": 3}


def test_failed_save_keeps_old_state(tmp_path):
    p = tmp_path / "s.json"
    save_state(p, {"watermark": "good"})
    with pytest.raises(TypeError):
        save_state(p, {"watermark": object()})
    assert load_state(p) == {"watermark": "good"}
    assert [f.name for f in tmp_path.iterdir()] == ["s.json"]
