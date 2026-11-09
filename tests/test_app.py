import importlib
from datetime import date, timedelta

import pytest


MODULES = ("paths", "db", "users", "content", "sql_content", "service", "sql_service", "app")


def reload_all():
    """Re-import the app's modules so they pick up TESTUDINES_* settings made by a test."""
    import testudines
    for name in MODULES:
        importlib.reload(importlib.import_module(f"testudines.{name}"))
    return testudines


@pytest.fixture()
def db(tmp_path):
    from testudines.db import DB
    return DB(tmp_path / "progress.db")


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
    from testudines import runner
    ok = runner.check({"solution.py": "def f():\n    return 1\n"},
                      {"test_f.py": "from solution import f\ndef test_f():\n    assert f() == 1\n"})
    assert ok["passed"]
    bad = runner.check({"solution.py": "def f():\n    return 2\n"},
                       {"test_f.py": "from solution import f\ndef test_f():\n    assert f() == 1\n"})
    assert not bad["passed"] and bad["n_failed"] == 1
    t = runner.run_main({"a.py": "while True: pass"}, "a.py", timeout=1)
    assert not t["ok"] and "stopped" in t["output"]


def test_runner_rejects_path_escape():
    from testudines import runner
    with pytest.raises(ValueError):
        runner.run_main({"../evil.py": "print(1)"}, "../evil.py")


def test_content_ids_unique_and_wellformed():
    from testudines.content import load_curriculum
    mods = load_curriculum()
    ids = [e.id for m in mods for l in m.lessons for e in l.exercises]
    assert len(ids) == len(set(ids))


def test_desktop_ui_opens_every_page(tmp_path, monkeypatch):
    monkeypatch.setenv("TESTUDINES_HOME", str(tmp_path))
    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
    t = reload_all()
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    win = t.app.MainWindow(t.users.add("Tester"))
    win.set_section("python")
    lid = win.svc.idx.lesson_order[0]
    eid = win.svc.idx.lessons[lid].exercises[0].id
    win.go_today(); win.go_map(); win.go_lesson(lid); win.go_exercise(eid)
    win.go_exercise(eid, redo=True); win.go_review(); win.go_scratch(); win.go_reference()
    app.processEvents()


def _fresh_service(monkeypatch, content, home):
    monkeypatch.setenv("TESTUDINES_CONTENT", str(content))
    monkeypatch.setenv("TESTUDINES_HOME", str(home))
    t = reload_all()
    return t.service.Service(t.db.DB(home / "progress.db"))


def test_progress_survives_renames_reordering_and_inserted_cards(tmp_path, monkeypatch):
    import re
    import shutil
    from pathlib import Path
    src = Path(__file__).resolve().parent.parent / "content" / "python" / "01-sql-to-python" / "01-foundations"
    content = tmp_path / "content"
    shutil.copytree(src, content / "python" / "01-foundations")
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
    from testudines.content import id_problems, load_curriculum
    src = Path(__file__).resolve().parent.parent / "content" / "python" / "01-sql-to-python" / "01-foundations"
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


def test_learning_paths_drive_today_and_the_curriculum(tmp_path, monkeypatch):
    import shutil
    from pathlib import Path
    src = Path(__file__).resolve().parent.parent / "content" / "python" / "01-sql-to-python" / "01-foundations"
    content = tmp_path / "content"
    for n, pid in ((1, "first"), (2, "second")):
        pd = content / "python" / f"0{n}-{pid}"
        shutil.copytree(src, pd / "01-foundations")
        (pd / "path.toml").write_text(f'id = "{pid}"\ntitle = "Path {n}"\nsummary = "s"\n')
    second = content / "python" / "02-second" / "01-foundations"
    for f in second.rglob("*"):  # give the second copy its own ids
        if f.is_file() and f.suffix in (".md", ".toml"):
            f.write_text(f.read_text().replace('id = "', 'id = "two.'))
    svc = _fresh_service(monkeypatch, content, tmp_path / "home")
    assert [p["id"] for p in svc.paths()] == ["first", "second"]
    assert svc.path == "first" and svc.today()["next_lesson"] == svc.idx.path_order["first"][0]
    svc.set_path("second")
    assert svc.today()["next_lesson"] == svc.idx.path_order["second"][0]
    assert svc.curriculum()["path"] == "second"
    last = svc.idx.path_order["second"][-1]
    assert svc.lesson(last)["next"] is None  # next never crosses into another path
    with pytest.raises(ValueError):
        svc.set_path("no-such-path")


# ---- learner code can't burden the computer
def test_runner_stops_endless_output_without_holding_it_in_memory():
    from testudines import runner
    r = runner.run_main({"a.py": "while True: print('x' * 1000)"}, "a.py", timeout=20)
    assert not r["ok"] and "printed more than" in r["output"] and len(r["output"]) < runner.MAX_OUT + 300


def test_runner_caps_learner_memory():
    from testudines import runner
    r = runner.run_main({"a.py": "x = []\nwhile True: x.append(b'x' * 20_000_000)"}, "a.py", timeout=20,
                        memory_mb=300)
    assert not r["ok"] and "300 MB" in r["output"]


def test_runner_default_memory_cap_fits_small_computers():
    from testudines import runner
    assert 512 <= runner.memory_limit_mb() <= 1536


def test_runner_stops_programs_learner_code_started():
    import time
    import psutil
    from testudines import runner
    code = ("import subprocess, sys, time\n"
            "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)  #testudines-child'])\n"
            "time.sleep(60)\n")
    r = runner.run_main({"a.py": code}, "a.py", timeout=2)
    assert "stopped" in r["output"]
    time.sleep(0.5)
    left = [p for p in psutil.process_iter(["name", "cmdline"])
            if (p.info["name"] or "").lower().startswith("python") and p.info["cmdline"]
            and p.info["cmdline"][-1].endswith("#testudines-child")]
    assert left == []
