"""The SQL section: grading, the curriculum files, the three ways to practice, progress, users."""
import importlib
import json

import pytest

from testudines import sql_grader
from testudines.sql_content import SqlIndex

SCHEMA = """
create table people (id integer, name varchar, team varchar);
insert into people values (1, 'Ana', 'red'), (2, 'Ben', null), (3, 'Cy', 'blue');
"""
SOLUTION = "select id, name from people where team is not null order by id;"


def test_grading_ignores_column_and_row_order():
    assert sql_grader.check(SCHEMA, SOLUTION, "select name, id from people where team is not null order by id desc")["passed"]


def test_grading_explains_a_wrong_result_and_an_error():
    wrong = sql_grader.check(SCHEMA, SOLUTION, "select id, name from people")
    assert not wrong["passed"] and wrong["message"].startswith("Not quite — expected 2 row(s), got 3")
    err = sql_grader.check(SCHEMA, SOLUTION, "select nope from people")
    assert not err["passed"] and err["message"].startswith("SQL error:")
    empty = sql_grader.check(SCHEMA, SOLUTION, "-- just a comment\n")
    assert not empty["passed"] and "Write a query first" in empty["message"]


def test_nulls_and_numbers_compare_as_values():
    assert sql_grader.check(SCHEMA, "select team from people", "select team from people")["passed"]
    assert sql_grader.check(SCHEMA, "select 2.0 as x", "select 2 as x")["passed"]
    assert not sql_grader.check(SCHEMA, "select team from people", "select coalesce(team, '') from people")["passed"]


def test_each_run_starts_from_fresh_tables():
    sql_grader.run(SCHEMA, "delete from people")
    assert len(sql_grader.run(SCHEMA, "select * from people").rows) == 3


def test_sample_tables_show_rows_and_totals():
    t = sql_grader.sample_tables(SCHEMA)
    assert [x["name"] for x in t] == ["people"] and t[0]["total"] == 3 and t[0]["columns"] == ["id", "name", "team"]


@pytest.fixture(scope="module")
def idx():
    return SqlIndex()


def test_the_curriculum_has_its_track_and_practice_families(idx):
    assert len(idx.lessons) == 20 and len(idx.track) == 100
    assert len(idx.families) == 10 and len(idx.extra) == 200
    assert idx.track[0].id == "1.1" and idx.extra[0].id == "extra-1"
    assert len(idx.by_id) == 300


def test_every_reference_passes_and_every_starter_doesnt(idx):
    bad = [e.id for e in idx.all if not sql_grader.check(e.schema, e.solution, e.solution)["passed"]
           or sql_grader.check(e.schema, e.solution, e.starter)["passed"]]
    assert bad == []


def test_an_exercise_uses_its_lesson_schema_unless_it_has_its_own(tmp_path):
    root = tmp_path / "sql"
    lesson = root / "track" / "01-basics"
    for n, own in ((1, False), (2, True)):
        ex = lesson / "exercises" / f"0{n}-x"
        ex.mkdir(parents=True)
        (ex / "exercise.toml").write_text(f'id = "t.{n}"\ntitle = "X"\ndifficulty = "easy"\n')
        (ex / "solution.sql").write_text("select 1;")
        if own:
            (ex / "schema.sql").write_text("create table own (a int);")
    (lesson / "lesson.toml").write_text('id = "l1"\ntitle = "Basics"\n')
    (lesson / "schema.sql").write_text("create table shared (a int);")
    i = SqlIndex(root)
    assert "shared" in i.by_id["t.1"].schema and "own" in i.by_id["t.2"].schema


@pytest.fixture()
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("TESTUDINES_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
    import testudines
    for name in ("paths", "db", "users", "sql_service", "service", "app"):
        importlib.reload(importlib.import_module(f"testudines.{name}"))
    return testudines


@pytest.fixture()
def sql(home, idx):
    return home.sql_service.SqlService(home.users.open_db(home.users.add("Ana")), idx)


def test_track_practice_and_randomizer_queues(sql, idx):
    track = sql.start("track")
    assert track["queue"] == [e.id for e in idx.track]
    practice = sql.start("practice", ["hard"], 5)
    assert practice["queue"] == [e.id for e in idx.all if e.difficulty == "hard"][:5]  # first five, in order
    every_easy = sql.start("practice", ["easy"], None)
    assert len(every_easy["queue"]) == sum(e.difficulty == "easy" for e in idx.all)
    rnd = sql.start("randomizer", None, 7)
    assert len(rnd["queue"]) == 7 == len(set(rnd["queue"]))
    with pytest.raises(ValueError):
        sql.start("practice", [], 3)


def test_sessions_are_saved_resumed_and_ended(sql):
    s = sql.start("practice", ["medium"], 4)
    sql.remember(s, s["queue"][2])
    again = sql.saved("practice")
    assert again["queue"] == s["queue"] and again["current"] == s["queue"][2]
    sql.end("practice")
    assert sql.saved("practice") is None
    t = sql.start("track")
    sql.remember(t, "2.3")
    assert sql.start("track")["current"] == "2.3"  # the track picks up where you left off


def test_solution_unlocks_after_three_failed_checks(sql, idx):
    e = idx.track[0]
    assert not sql.exercise(e.id)["solution_available"]
    for _ in range(3):
        res = sql.check(e.id, "select 1")
    assert res["solution_available"] and "Show solution" in res["message"]
    good = sql.check(e.id, e.solution)
    assert good["passed"] and sql.exercise(e.id)["completed"] and sql.exercise(e.id)["code"] == e.solution


def test_progress_is_dropped_when_an_exercise_changes(sql, idx):
    e = idx.track[1]
    sql.check(e.id, e.solution)
    sql.db.sql_put(e.id, fingerprint="an older solution")
    st = sql.exercise(e.id)
    assert not st["completed"] and st["code"] == e.starter


def test_export_and_import_including_a_sql_dojo_file(sql, idx):
    a, b = idx.track[0], idx.track[1]
    sql.check(a.id, a.solution)
    exported = sql.export()
    assert exported[a.id]["completed"] and exported[a.id]["code"] == a.solution
    sql_dojo_file = {a.id: {"completed": True, "code": "select 1", "failCount": 0, "contentFingerprint": a.solution},
                     b.id: {"completed": True, "code": "x", "failCount": 2, "contentFingerprint": "changed since"},
                     "no-such-exercise": {"completed": True}}
    assert sql.import_progress(json.loads(json.dumps(sql_dojo_file))) == 2
    assert sql.exercise(a.id)["completed"] and sql.exercise(a.id)["code"] == "select 1"
    assert not sql.exercise(b.id)["completed"] and sql.exercise(b.id)["fail_count"] == 2
    with pytest.raises(ValueError):
        sql.import_progress({"not": "progress"})


def test_each_user_has_their_own_progress(home, idx):
    users = home.users
    ana = home.sql_service.SqlService(users.open_db(users.add("Ana")), idx)
    ben = home.sql_service.SqlService(users.open_db(users.add("Ben")), idx)
    ana.check(idx.track[0].id, idx.track[0].solution)
    assert ana.completed() == {idx.track[0].id} and ben.completed() == set()
    assert users.users() == ["Ana", "Ben"] and users.folder("Ana") != users.folder("Ben")


def test_the_first_user_takes_over_py_dojo_progress(home, tmp_path, monkeypatch):
    old = tmp_path / "PyDojo"
    old.mkdir()
    from testudines.db import DB
    DB(old / "progress.db").mark_read("lesson-x")
    (old / "scratch.py").write_text("print('mine')")
    monkeypatch.setattr(home.users, "PY_DOJO_HOME", old)
    first = home.users.add("Ana")
    assert "lesson-x" in home.users.open_db(first).lessons_read()
    assert (home.users.folder(first) / "scratch.py").read_text() == "print('mine')"
    second = home.users.add("Ben")
    assert home.users.open_db(second).lessons_read() == set()


def test_sql_screens_open_and_pause(home, idx):
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    win = home.app.MainWindow(home.users.add("Ana"), sql_index=idx)
    win.set_section("sql")
    for mode, diffs, count in (("track", None, None), ("practice", ["easy"], 3), ("randomizer", None, 3)):
        win.sql_start(mode, diffs, count)
        app.processEvents()
        assert win.sql_exercise.queue_list.isVisibleTo(win.sql_exercise) == (mode != "randomizer")
    page = win.sql_exercise
    page.pause()
    assert page.paused and page.layers.currentIndex() == 1
    page.resume()
    assert not page.paused
    page.editor.setPlainText("select 1")
    page._save()
    assert win.sql.exercise(page.eid)["code"] == "select 1"
    win.go_sql_home()
    app.processEvents()


def test_queries_are_kept_small():
    assert sql_grader.CONFIG["threads"] == 2 and sql_grader.memory_limit_mb() <= 256
    big = sql_grader.run(SCHEMA, "select * from range(300000)")
    assert big.truncated and len(big.rows) == sql_grader.MAX_ROWS
    res = sql_grader.check(SCHEMA, SOLUTION, "select * from range(300000)")
    assert not res["passed"] and "more than" in res["message"]


def test_queries_cant_reach_files():
    assert "disabled" in sql_grader.run(SCHEMA, "select * from read_csv('pyproject.toml')").error


def test_a_runaway_query_is_stopped(monkeypatch):
    monkeypatch.setattr(sql_grader, "QUERY_SECONDS", 1)
    r = sql_grader.run(SCHEMA, "select count(*) from range(100000000000) a, range(100000) b")
    assert "stopped after 1 seconds" in r.error
