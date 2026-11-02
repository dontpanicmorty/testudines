import importlib
from datetime import date, timedelta

import pytest


@pytest.fixture()
def db(tmp_path, monkeypatch):
    monkeypatch.setenv("PYDOJO_HOME", str(tmp_path))
    import pydojo.paths, pydojo.db
    importlib.reload(pydojo.paths)
    importlib.reload(pydojo.db)
    return pydojo.db.DB()


def test_srs_intervals_grow_then_reset(db):
    db.srs_enroll("card:x:0", "card")
    days = []
    for _ in range(4):
        r = db.srs_grade("card:x:0", "good")
        days.append((date.fromisoformat(r["due"]) - date.today()).days)
    assert days[0] == 1 and days[1] == 3 and days[2] > days[1] and days[3] > days[2]
    r = db.srs_grade("card:x:0", "again")
    assert (date.fromisoformat(r["due"]) - date.today()).days == 1
    assert db.srs_get("card:x:0")["reps"] == 0


def test_due_filtering(db):
    db.srs_enroll("card:a:0", "card")
    db.srs_enroll("card:b:0", "card", first_due_days=5)
    assert db.srs_due("card", 10) == ["card:a:0"]


def test_streak(db):
    db.bump("review")
    assert db.streak() == 1


def test_runner_pass_fail_and_timeout():
    from pydojo import runner
    ok = runner.check({"solution.py": "def f():\n    return 1\n"},
                      {"test_f.py": "from solution import f\ndef test_f():\n    assert f() == 1\n"})
    assert ok["passed"]
    bad = runner.check({"solution.py": "def f():\n    return 2\n"},
                       {"test_f.py": "from solution import f\ndef test_f():\n    assert f() == 1\n"})
    assert not bad["passed"] and bad["n_failed"] == 1
    t = runner.run_main({"a.py": "while True: pass"}, "a.py", timeout=1)
    assert not t["ok"] and "stopped" in t["output"]


def test_runner_rejects_path_escape():
    from pydojo import runner
    with pytest.raises(ValueError):
        runner.run_main({"../evil.py": "print(1)"}, "../evil.py")


def test_content_ids_unique_and_wellformed():
    from pydojo.content import load_curriculum
    mods = load_curriculum()
    ids = [e.id for m in mods for l in m.lessons for e in l.exercises]
    assert len(ids) == len(set(ids))


def test_desktop_ui_opens_every_page(tmp_path, monkeypatch):
    monkeypatch.setenv("PYDOJO_HOME", str(tmp_path))
    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
    import importlib
    import pydojo.paths, pydojo.db, pydojo.service
    for m in (pydojo.paths, pydojo.db, pydojo.service):
        importlib.reload(m)
    from PySide6.QtWidgets import QApplication
    from pydojo.app import MainWindow
    app = QApplication.instance() or QApplication([])
    win = MainWindow(pydojo.service.Service())
    lid = win.svc.idx.lesson_order[0]
    eid = win.svc.idx.lessons[lid].exercises[0].id
    win.go_today(); win.go_map(); win.go_lesson(lid); win.go_exercise(eid)
    win.go_exercise(eid, redo=True); win.go_review(); win.go_scratch(); win.go_reference()
    app.processEvents()


def _fresh_service(monkeypatch, content, home):
    monkeypatch.setenv("PYDOJO_CONTENT", str(content))
    monkeypatch.setenv("PYDOJO_HOME", str(home))
    import pydojo.paths, pydojo.db, pydojo.content, pydojo.service
    for m in (pydojo.paths, pydojo.db, pydojo.content, pydojo.service):
        importlib.reload(m)
    return pydojo.service.Service()


def test_progress_survives_renames_reordering_and_inserted_cards(tmp_path, monkeypatch):
    import re
    import shutil
    from pathlib import Path
    src = Path(__file__).resolve().parent.parent / "content" / "01-foundations"
    content = tmp_path / "content"
    shutil.copytree(src, content / "01-foundations")
    svc = _fresh_service(monkeypatch, content, tmp_path / "home")
    lid = svc.idx.lesson_order[0]
    svc.read_lesson(lid)
    item = svc.today()["cards"][0]["item"]
    q_before = svc.card(item)["q"]
    svc.db.srs_grade(item, "good")
    ex = svc.idx.lessons[lid].exercises[0]
    svc.db.record_attempt(ex.id, True)

    # restructure the content: rename lesson + exercise folders, reverse card order, add a card on top
    lesson_dir = svc.idx.lessons[lid].dir
    ex_dir = ex.dir
    new_ex = ex_dir.rename(ex_dir.parent / "99-renamed-exercise")
    new_lesson = lesson_dir.rename(lesson_dir.parent / "50-totally-renamed-lesson")
    cards = new_lesson / "cards.toml"
    blocks = re.split(r"(?m)^(?=\[\[card\]\])", cards.read_text())
    blocks = [b for b in blocks if b.strip()]
    inserted = '[[card]]\nid = "brand-new-1"\nq = "new q"\na = "new a"\n\n'
    cards.write_text(inserted + "".join(reversed(blocks)))

    svc2 = _fresh_service(monkeypatch, content, tmp_path / "home")
    assert lid in svc2.idx.lessons, "lesson id must not depend on its folder name"
    assert svc2.idx.exercises[ex.id].dir.name == "99-renamed-exercise"
    assert svc2.card(item)["q"] == q_before, "a card keeps its identity when cards are reordered/inserted"
    assert svc2.db.srs_get(item)["reps"] == 1, "its review schedule is untouched"
    assert ex.id in svc2.db.exercises_passed()
    assert lid in svc2.db.lessons_read()


def test_id_problems_reports_missing_and_duplicates(tmp_path, monkeypatch):
    import shutil
    from pathlib import Path
    from pydojo.content import id_problems, load_curriculum
    src = Path(__file__).resolve().parent.parent / "content" / "01-foundations"
    root = tmp_path / "c"
    shutil.copytree(src, root / "01-foundations")
    assert id_problems(load_curriculum(root)) == []
    lessons = sorted((root / "01-foundations").glob("*/lesson.md"))
    text = lessons[1].read_text()
    first_id = lessons[0].read_text().split('id = "')[1].split('"')[0]
    lessons[1].write_text(text.replace(text.split('id = "')[1].split('"')[0], first_id, 1))   # duplicate
    cards = next((root / "01-foundations").glob("*/cards.toml"))
    cards.write_text(cards.read_text().replace('id = ', '#id = ', 1))                          # missing
    problems = "\n".join(id_problems(load_curriculum(root)))
    assert "DUPLICATE" in problems and "MISSING card id" in problems
