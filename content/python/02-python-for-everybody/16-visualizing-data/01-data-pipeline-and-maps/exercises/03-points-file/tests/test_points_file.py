import json
import sqlite3

import pytest

from solution import write_points_js


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE place (name TEXT PRIMARY KEY, lat REAL, lon REAL)")
    return c


def test_exact_text(conn, tmp_path):
    conn.executemany("INSERT INTO place VALUES (?, ?, ?)", [("Oakby", 51.5, -1.1), ("Larkfield", 51.2, -1.4)])
    out = tmp_path / "points.js"
    assert write_points_js(conn, out) == 2
    assert out.read_text(encoding="utf-8") == 'var points = [["Larkfield", 51.2, -1.4], ["Oakby", 51.5, -1.1]];\n'


def test_empty(conn, tmp_path):
    out = tmp_path / "p.js"
    assert write_points_js(conn, str(out)) == 0
    assert out.read_text(encoding="utf-8") == "var points = [];\n"


def test_special_characters_stay_valid(conn, tmp_path):
    conn.execute("INSERT INTO place VALUES (?, ?, ?)", ('O\'Neil "Quay"', 1.0, 2.0))
    out = tmp_path / "p.js"
    write_points_js(conn, out)
    text = out.read_text(encoding="utf-8")
    payload = text[len("var points = "):].strip().rstrip(";")
    assert json.loads(payload) == [['O\'Neil "Quay"', 1.0, 2.0]]
