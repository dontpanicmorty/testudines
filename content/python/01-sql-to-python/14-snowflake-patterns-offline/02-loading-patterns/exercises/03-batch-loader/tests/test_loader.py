import pytest

from solution import load_rows


class Cur:
    def __init__(self, conn):
        self.conn, self.closed = conn, False

    def executemany(self, sql, batch):
        self.conn.events.append(("many", sql, list(batch)))
        if self.conn.fail_on is not None and len([e for e in self.conn.events if e[0] == "many"]) == self.conn.fail_on:
            raise ValueError("bad batch")

    def execute(self, sql, params=None):
        raise AssertionError("use executemany for batches")

    def close(self):
        self.closed = True


class Conn:
    def __init__(self, fail_on=None):
        self.events, self.fail_on, self.cur = [], fail_on, None

    def cursor(self):
        self.cur = Cur(self)
        return self.cur

    def commit(self):
        self.events.append(("commit",))

    def rollback(self):
        self.events.append(("rollback",))


def rows(n):
    return ({"order_id": i, "status": "open", "ignored": "x"} for i in range(n))


def test_batches_and_sql():
    conn = Conn()
    n = load_rows(conn, "orders", ["order_id", "status"], rows(5), batch_size=2)
    assert n == 5
    manys = [e for e in conn.events if e[0] == "many"]
    assert [len(e[2]) for e in manys] == [2, 2, 1]
    assert manys[0][1] == "INSERT INTO orders (order_id, status) VALUES (%s, %s)"
    assert manys[0][2][0] == (0, "open")


def test_single_commit_at_end():
    conn = Conn()
    load_rows(conn, "t", ["order_id"], rows(5), batch_size=2)
    kinds = [e[0] for e in conn.events]
    assert kinds.count("commit") == 1 and kinds[-1] == "commit"
    assert "rollback" not in kinds
    assert conn.cur.closed


def test_failure_rolls_back_without_commit():
    conn = Conn(fail_on=2)
    with pytest.raises(ValueError, match="bad batch"):
        load_rows(conn, "t", ["order_id"], rows(10), batch_size=3)
    kinds = [e[0] for e in conn.events]
    assert "commit" not in kinds
    assert kinds[-1] == "rollback"
    assert conn.cur.closed


def test_empty_rows():
    conn = Conn()
    assert load_rows(conn, "t", ["a"], []) == 0
    assert [e[0] for e in conn.events].count("many") == 0


def test_does_not_consume_all_rows_up_front():
    pulled = []

    def gen():
        for i in range(6):
            pulled.append(i)
            yield {"a": i}

    class Probe(Conn):
        def cursor(self):
            c = super().cursor()
            orig = c.executemany

            def spy(sql, batch):
                self.events.append(("seen", len(pulled)))
                orig(sql, batch)

            c.executemany = spy
            return c

    conn = Probe()
    load_rows(conn, "t", ["a"], gen(), batch_size=2)
    seen = [e[1] for e in conn.events if e[0] == "seen"]
    assert seen == [2, 4, 6], f"rows pulled at each batch: {seen}"
