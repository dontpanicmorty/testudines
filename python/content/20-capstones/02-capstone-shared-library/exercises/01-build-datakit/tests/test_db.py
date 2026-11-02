import pytest

from datakit import ConnectionProtocol, DatabaseError, DatakitError, SqliteConnection


def seeded():
    conn = SqliteConnection()
    conn.execute("create table orders(order_id integer primary key, status text)")
    conn.executemany("insert into orders values (?, ?)", [(1, "open"), (2, "closed")])
    return conn


def row_count(conn: ConnectionProtocol, table: str) -> int:
    """A consumer function written against the protocol only."""
    return conn.query(f"select count(*) as n from {table}")[0]["n"]


def test_query_returns_list_of_dicts():
    assert seeded().query("select * from orders order by order_id") == [
        {"order_id": 1, "status": "open"}, {"order_id": 2, "status": "closed"}]


def test_query_params():
    assert seeded().query("select status from orders where order_id = ?", (2,)) == [{"status": "closed"}]


def test_execute_returns_rowcount():
    conn = seeded()
    assert conn.execute("update orders set status = ? where order_id = ?", ("shipped", 1)) == 1
    assert conn.execute("update orders set status = 'x' where order_id = 99") == 0


def test_satisfies_protocol():
    assert isinstance(SqliteConnection(), ConnectionProtocol)


def test_consumer_works_with_a_fake_connection():
    class FakeConnection:
        def query(self, sql, params=()):
            return [{"n": 42}]

        def execute(self, sql, params=()):
            return 0

        def close(self):
            pass

    fake = FakeConnection()
    assert isinstance(fake, ConnectionProtocol)
    assert row_count(fake, "whatever") == 42


def test_object_missing_methods_is_not_a_connection():
    class Half:
        def query(self, sql, params=()):
            return []

    assert not isinstance(Half(), ConnectionProtocol)


def test_sql_errors_become_database_error_with_cause():
    conn = seeded()
    with pytest.raises(DatabaseError) as exc:
        conn.query("select * from nope")
    assert exc.value.__cause__ is not None
    with pytest.raises(DatabaseError):
        conn.execute("insert into orders values (1, 'dup')")
    assert issubclass(DatabaseError, DatakitError)


def test_transaction_commits_on_success(tmp_path):
    path = str(tmp_path / "t.db")
    conn = SqliteConnection(path)
    conn.execute("create table t(x integer)")
    with conn.transaction():
        conn.execute("insert into t values (1)")
        conn.execute("insert into t values (2)")
    conn.close()
    assert row_count(SqliteConnection(path), "t") == 2


def test_transaction_rolls_back_on_error():
    conn = SqliteConnection()
    conn.execute("create table t(x integer)")
    with pytest.raises(RuntimeError):
        with conn.transaction():
            conn.execute("insert into t values (1)")
            raise RuntimeError("boom")
    assert row_count(conn, "t") == 0


def test_nested_transactions_join_the_outer_one():
    conn = SqliteConnection()
    conn.execute("create table t(x integer)")
    with pytest.raises(RuntimeError):
        with conn.transaction():
            with conn.transaction():
                conn.execute("insert into t values (1)")
            raise RuntimeError("outer fails")
    assert row_count(conn, "t") == 0


def test_autocommit_outside_transaction(tmp_path):
    path = str(tmp_path / "a.db")
    conn = SqliteConnection(path)
    conn.execute("create table t(x integer)")
    conn.execute("insert into t values (1)")
    other = SqliteConnection(path)
    assert row_count(other, "t") == 1


def test_context_manager_closes():
    with SqliteConnection() as conn:
        conn.execute("create table t(x integer)")
    with pytest.raises(Exception):
        conn.query("select 1")


def test_file_database_persists(tmp_path):
    path = str(tmp_path / "p.db")
    with SqliteConnection(path) as conn:
        conn.execute("create table t(x integer)")
        conn.execute("insert into t values (7)")
    with SqliteConnection(path) as conn:
        assert conn.query("select x from t") == [{"x": 7}]
