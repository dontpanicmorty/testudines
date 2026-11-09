"""`testudines selftest`: proves an installed copy works end to end (also a handy diagnostic)."""
from __future__ import annotations

import os
import sys
import tempfile


def main() -> int:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("TESTUDINES_HOME", tempfile.mkdtemp(prefix="testudines-selftest-"))
    from PySide6.QtWidgets import QApplication

    from . import runner, sql_grader, users
    from .app import MainWindow
    from .paths import CONTENT_DIR, DATASETS_DIR, HOME_DIR

    print(f"python      {sys.version.split()[0]}  ({sys.executable})")
    print(f"content     {CONTENT_DIR}")
    print(f"datasets    {DATASETS_DIR}")
    print(f"user data   {HOME_DIR}")
    app = QApplication.instance() or QApplication([])
    user = users.add("Selftest")
    win = MainWindow(user)
    svc, sql = win.svc, win.sql
    assert svc.idx.modules and svc.idx.exercises, "no Python content found"
    assert sql.idx.track and sql.idx.extra, "no SQL content found"

    # Python section: every page, and grading with pytest
    win.set_section("python")
    lid = svc.idx.lesson_order[0]
    eid = svc.idx.lessons[lid].exercises[0].id
    for go in (win.go_today, win.go_map, lambda: win.go_lesson(lid), lambda: win.go_exercise(eid),
               win.go_review, win.go_scratch, win.go_reference):
        go()
        app.processEvents()
    for path in svc.idx.paths:  # the Curriculum page on every learning path
        svc.set_path(path.id)
        win.go_map()
        app.processEvents()
        assert svc.curriculum()["modules"], f"path {path.id} has no modules"
    svc.set_path(svc.idx.paths[0].id)
    ex = svc.idx.exercises[eid]
    res = runner.check(ex.reference(), ex.tests())
    assert res["passed"], res["output"]
    libs = runner.run_scratch(
        "import duckdb, polars, pandas, pydantic, fastapi, httpx, typer, yaml, tenacity, mypy, ruff, bs4\n"
        "print('learner libraries ok')")
    if not libs["ok"]:  # the first run after installing can be slow (e.g. Rosetta translating it); retry once
        libs = runner.run_scratch(
            "import duckdb, polars, pandas, pydantic, fastapi, httpx, typer, yaml, tenacity, mypy, ruff, bs4\n"
            "print('learner libraries ok')", timeout=60)
    assert libs["ok"], libs["output"] or "the learner libraries failed to import, with no output"

    # SQL section: home, every mode, and grading with DuckDB
    win.set_section("sql")
    app.processEvents()
    for mode, diffs, count in (("track", None, None), ("practice", ["easy"], 3), ("randomizer", None, 3)):
        win.sql_start(mode, diffs, count)
        app.processEvents()
        assert win.sql_exercise.eid, mode
    first = sql.idx.track[0]
    good = sql.check(first.id, first.solution)
    assert good["passed"], good["message"]
    assert not sql.check(first.id, "select 1")["passed"]
    assert sql_grader.sample_tables(first.schema), "no sample tables"
    win.go_sql_home()
    app.processEvents()
    for path in svc.idx.paths:
        print(f"Python path {path.title!r}: {len(path.modules)} modules, "
              f"{sum(len(l.exercises) for m in path.modules for l in m.lessons)} exercises")
    print(f"Python: {len(svc.idx.modules)} modules, {len(svc.idx.exercises)} exercises, grading ok, "
          f"{libs['output'].strip()}")
    print(f"SQL: {len(sql.idx.track)} track + {len(sql.idx.extra)} practice exercises, grading ok")
    print("selftest ok")
    return 0
