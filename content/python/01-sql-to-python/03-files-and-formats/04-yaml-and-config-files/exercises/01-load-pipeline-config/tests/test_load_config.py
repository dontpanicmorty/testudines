import pytest

from solution import load_config


def write(tmp_path, text):
    p = tmp_path / "c.yml"
    p.write_text(text, encoding="utf-8")
    return p


def test_defaults_and_extras(tmp_path):
    cfg = load_config(write(tmp_path, "name: daily\nretries: 5\nowner: data-eng\n"))
    assert cfg == {"name": "daily", "retries": 5, "sources": [], "owner": "data-eng"}


def test_all_defaults(tmp_path):
    cfg = load_config(write(tmp_path, "name: x\n"))
    assert cfg == {"name": "x", "retries": 3, "sources": []}


def test_name_required(tmp_path):
    with pytest.raises(KeyError):
        load_config(write(tmp_path, "retries: 2\n"))


def test_empty_file_means_missing_name(tmp_path):
    with pytest.raises(KeyError):
        load_config(write(tmp_path, ""))
