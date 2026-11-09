import sqlite3

import pytest

from solution import bikes_at


@pytest.fixture
def db(tmp_path):
    path = str(tmp_path / "b.db")
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE reading (station TEXT, bikes INTEGER)")
    conn.executemany("INSERT INTO reading VALUES (?, ?)", [
        ("Mill Lane", 4), ("Hill Top", 9), ("Mill Lane", 7), ("O'Neil Quay", 2),
    ])
    conn.commit()
    conn.close()
    return path


def test_latest_row_wins(db):
    assert bikes_at(db, "Mill Lane") == 7


def test_single_row(db):
    assert bikes_at(db, "Hill Top") == 9


def test_unknown(db):
    assert bikes_at(db, "Nowhere") is None


def test_quote_in_name(db):
    assert bikes_at(db, "O'Neil Quay") == 2


def test_injection_is_just_text(db):
    assert bikes_at(db, "x' OR '1'='1") is None
