import sqlite3
import pytest
from solution import open_db


def test_idempotent_and_persistent(tmp_path):
    p = tmp_path / "x.db"
    c1 = open_db(p)
    c1.execute("INSERT INTO runs (started) VALUES ('2025-01-01')")
    c1.commit()
    c1.close()
    c2 = open_db(p)  # must not fail on the second call
    assert c2.execute("SELECT started FROM runs").fetchone()["started"] == "2025-01-01"


def test_foreign_keys_enforced(tmp_path):
    c = open_db(tmp_path / "x.db")
    assert c.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    with pytest.raises(sqlite3.IntegrityError):
        c.execute("INSERT INTO run_rows (run_id, payload) VALUES (999, 'x')")


def test_both_tables_exist(tmp_path):
    c = open_db(tmp_path / "x.db")
    names = {r["name"] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"runs", "run_rows"} <= names
