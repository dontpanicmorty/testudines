import pytest

from solution import daily_total


class Cur:
    def __init__(self, conn):
        self.conn, self.closed = conn, False
        conn.cursors.append(self)

    def execute(self, sql, params=None):
        self.conn.calls.append((" ".join(sql.split()), params))
        if self.conn.fail:
            raise RuntimeError("warehouse suspended")

    def fetchone(self):
        return self.conn.row

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class Conn:
    def __init__(self, row=None, fail=False):
        self.row, self.fail, self.calls, self.cursors, self.closed = row, fail, [], [], False

    def cursor(self):
        return Cur(self)

    def close(self):
        self.closed = True


def test_returns_float_and_binds_param():
    conn = Conn((125,))
    assert daily_total(lambda: conn, "2026-11-02") == 125.0
    assert isinstance(daily_total(lambda: Conn((1,)), "d"), float)
    sql, params = conn.calls[0]
    assert sql == "SELECT SUM(amount) FROM orders WHERE order_date = %(day)s"
    assert params == {"day": "2026-11-02"}


def test_null_sum_is_zero():
    assert daily_total(lambda: Conn((None,)), "d") == 0.0


def test_closes_connection_and_cursor():
    conn = Conn((1,))
    daily_total(lambda: conn, "d")
    assert conn.closed and all(c.closed for c in conn.cursors)


def test_closes_on_error_and_propagates():
    conn = Conn(fail=True)
    with pytest.raises(RuntimeError, match="suspended"):
        daily_total(lambda: conn, "d")
    assert conn.closed
