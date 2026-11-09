import pytest

from solution import run_tasks


def recorder(log, name, fail=False):
    def task():
        log.append(name)
        if fail:
            raise RuntimeError(name)
    return task


def test_runs_in_dependency_order():
    log = []
    tasks = {n: recorder(log, n) for n in "dcba"}
    deps = {"d": ["b", "c"], "b": ["a"], "c": ["a"]}
    status = run_tasks(tasks, deps)
    assert log == ["a", "b", "c", "d"]
    assert set(status.values()) == {"success"}


def test_failure_skips_downstream_but_not_unrelated():
    log = []
    tasks = {
        "a": recorder(log, "a", fail=True),
        "b": recorder(log, "b"),
        "c": recorder(log, "c"),
        "d": recorder(log, "d"),
    }
    deps = {"b": ["a"], "d": ["b", "c"]}
    status = run_tasks(tasks, deps)
    assert status == {"a": "failed", "b": "skipped", "c": "success", "d": "skipped"}
    assert log == ["a", "c"], "skipped tasks must not be called"


def test_independent_failure_does_not_stop_run():
    log = []
    tasks = {"a": recorder(log, "a", fail=True), "b": recorder(log, "b")}
    assert run_tasks(tasks, {}) == {"a": "failed", "b": "success"}


def test_cycle_detected_before_running():
    log = []
    tasks = {"a": recorder(log, "a"), "b": recorder(log, "b"), "c": recorder(log, "c")}
    with pytest.raises(ValueError, match="cycle"):
        run_tasks(tasks, {"a": ["b"], "b": ["a"]})
    assert log == []


def test_empty():
    assert run_tasks({}, {}) == {}
