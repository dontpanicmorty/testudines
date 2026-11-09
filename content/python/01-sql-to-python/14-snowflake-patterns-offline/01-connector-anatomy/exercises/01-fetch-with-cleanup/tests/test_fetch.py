import pytest

from solution import fetch_all, scalar


class Cur:
    def __init__(self, conn):
        self.conn, self.closed = conn, False
        conn.cursors.append(self)

    def execute(self, sql, params=None):
        self.conn.log.append((sql, params))
        if self.conn.fail:
            raise RuntimeError("boom")
        return self

    def fetchall(self):
        return list(self.conn.rows)

    def fetchone(self):
        return self.conn.rows[0] if self.conn.rows else None

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


class Conn:
    def __init__(self, rows=(), fail=False):
        self.rows, self.fail, self.log, self.cursors = list(rows), fail, [], []

    def cursor(self):
        return Cur(self)


def test_fetch_all_returns_rows_and_passes_params():
    conn = Conn([(1, "Ada"), (2, "Linus")])
    assert fetch_all(conn, "SELECT 1 WHERE x = %(x)s", {"x": 5}) == [(1, "Ada"), (2, "Linus")]
    assert conn.log == [("SELECT 1 WHERE x = %(x)s", {"x": 5})]


def test_cursor_closed_after_success():
    conn = Conn([(1,)])
    fetch_all(conn, "SELECT 1")
    scalar(conn, "SELECT 1")
    assert conn.cursors and all(c.closed for c in conn.cursors)


def test_cursor_closed_when_execute_fails():
    conn = Conn(fail=True)
    with pytest.raises(RuntimeError):
        fetch_all(conn, "SELECT 1")
    with pytest.raises(RuntimeError):
        scalar(conn, "SELECT 1")
    assert all(c.closed for c in conn.cursors), "cursor leaked after an error"


def test_scalar_value_and_default():
    assert scalar(Conn([(42, "x")]), "SELECT 42") == 42
    assert scalar(Conn([]), "SELECT MAX(x)", default="none") == "none"
    assert scalar(Conn([]), "SELECT MAX(x)") is None
