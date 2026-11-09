from solution import Pipeline


def test_record_and_read():
    p = Pipeline("orders")
    p.record_error("timeout")
    p.record_error("bad row")
    assert p.errors == ["orders: timeout", "orders: bad row"]
    assert p.failed() is True


def test_fresh_pipeline_has_no_errors():
    assert Pipeline("x").errors == []
    assert Pipeline("x").failed() is False


def test_pipelines_do_not_share_errors():
    a, b = Pipeline("orders"), Pipeline("customers")
    a.record_error("timeout")
    assert b.errors == []
    assert b.failed() is False
    assert a.failed() is True


def test_later_instances_start_clean():
    first = Pipeline("a")
    first.record_error("x")
    second = Pipeline("b")
    assert second.errors == []
