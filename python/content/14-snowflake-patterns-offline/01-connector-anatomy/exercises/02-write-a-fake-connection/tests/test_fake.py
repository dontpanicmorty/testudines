import pytest

from solution import FakeConnection

SET1 = [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Linus"}, {"id": 3, "name": "Grace"}]


def test_fetch_variants_advance():
    conn = FakeConnection([SET1])
    cur = conn.cursor()
    assert cur.execute("SELECT 1") is cur
    assert cur.fetchone() == (1, "Ada")
    assert cur.fetchmany(1) == [(2, "Linus")]
    assert cur.fetchall() == [(3, "Grace")]
    assert cur.fetchone() is None
    assert cur.fetchall() == []


def test_fetchmany_larger_than_remaining():
    cur = FakeConnection([SET1]).cursor()
    cur.execute("q")
    assert cur.fetchmany(10) == [(1, "Ada"), (2, "Linus"), (3, "Grace")]


def test_description_and_rowcount():
    cur = FakeConnection([SET1]).cursor()
    assert cur.description is None
    cur.execute("q")
    assert [d[0] for d in cur.description] == ["ID", "NAME"]
    assert all(len(d) == 7 for d in cur.description)
    assert cur.rowcount == 3


def test_empty_result_set():
    cur = FakeConnection([[]]).cursor()
    cur.execute("INSERT ...")
    assert cur.description is None
    assert cur.fetchone() is None
    assert cur.rowcount == 0


def test_script_consumed_in_order_across_cursors():
    conn = FakeConnection([[{"a": 1}], [{"a": 2}]])
    c1, c2 = conn.cursor(), conn.cursor()
    c1.execute("first", {"x": 1})
    c2.execute("second")
    assert c2.fetchall() == [(2,)] and c1.fetchall() == [(1,)]
    assert conn.executed == [("first", {"x": 1}), ("second", None)]


def test_exhausted_script_raises():
    cur = FakeConnection([]).cursor()
    with pytest.raises(RuntimeError, match="no scripted result"):
        cur.execute("SELECT nothing")


def test_context_managers_close_and_commit():
    conn = FakeConnection([SET1])
    with conn:
        with conn.cursor() as cur:
            cur.execute("q")
        assert cur.closed and not conn.closed
        conn.commit()
        conn.commit()
    assert conn.closed and conn.commits == 2


def test_script_not_mutated_for_caller():
    script = [SET1]
    FakeConnection(script).cursor().execute("q")
    assert script == [SET1], "the caller's script list should be left intact"
