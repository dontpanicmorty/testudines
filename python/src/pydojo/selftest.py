"""`pydojo selftest`: proves an installed copy works end to end (also a handy diagnostic)."""
from __future__ import annotations

import os
import sys


def main() -> int:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication

    from . import runner
    from .app import MainWindow
    from .paths import CONTENT_DIR, DATASETS_DIR, HOME_DIR
    from .service import Service

    print(f"python      {sys.version.split()[0]}  ({sys.executable})")
    print(f"content     {CONTENT_DIR}")
    print(f"datasets    {DATASETS_DIR}")
    print(f"user data   {HOME_DIR}")
    app = QApplication.instance() or QApplication([])
    svc = Service()
    mods = svc.idx.modules
    n_ex = len(svc.idx.exercises)
    assert mods and n_ex, "no content found"
    win = MainWindow(svc)
    lid = svc.idx.lesson_order[0]
    eid = svc.idx.lessons[lid].exercises[0].id
    for go in (win.go_today, win.go_map, lambda: win.go_lesson(lid), lambda: win.go_exercise(eid),
               win.go_review, win.go_scratch, win.go_reference):
        go()
        app.processEvents()
    ex = svc.idx.exercises[eid]
    res = runner.check(ex.reference(), ex.tests())
    assert res["passed"], res["output"]
    libs = runner.run_scratch(
        "import duckdb, polars, pandas, pydantic, fastapi, httpx, typer, yaml, tenacity, mypy, ruff\n"
        "print('learner libraries ok')")
    assert libs["ok"], libs["output"]
    print(f"{len(mods)} modules, {n_ex} exercises, grading ok, {libs['output'].strip()}")
    print("selftest ok")
    return 0
