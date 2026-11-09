import sqlite3

import pytest

from solution import locate


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE place (name TEXT PRIMARY KEY, lat REAL, lon REAL)")
    return c


def make_geocoder():
    calls = []
    table = {"Larkfield": (51.2, -1.4), "Oakby": (51.5, -1.1)}

    def geocoder(name):
        calls.append(name)
        return table[name]

    return geocoder, calls


def test_first_call_asks(conn):
    g, calls = make_geocoder()
    assert locate(conn, "Larkfield", g) == (51.2, -1.4)
    assert calls == ["Larkfield"]


def test_second_call_uses_cache(conn):
    g, calls = make_geocoder()
    locate(conn, "Larkfield", g)
    assert locate(conn, "Larkfield", g) == (51.2, -1.4)
    assert calls == ["Larkfield"]


def test_different_names(conn):
    g, calls = make_geocoder()
    locate(conn, "Larkfield", g)
    locate(conn, "Oakby", g)
    locate(conn, "Oakby", g)
    assert calls == ["Larkfield", "Oakby"]
    assert conn.execute("SELECT COUNT(*) FROM place").fetchone()[0] == 2


def test_prefilled_row_never_asks(conn):
    conn.execute("INSERT INTO place VALUES ('Known', 1.5, 2.5)")
    g, calls = make_geocoder()
    assert locate(conn, "Known", g) == (1.5, 2.5)
    assert calls == []
