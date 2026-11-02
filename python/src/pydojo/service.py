"""Application service layer: curriculum views, grading, progress. No UI, no network."""
from __future__ import annotations

import json
import threading
from pathlib import Path

from . import runner
from .content import Index
from .db import DB
from .paths import CONTENT_DIR

REDO_STEPS = [1, 3, 7, 16, 35, 90]


class Service:
    def __init__(self) -> None:
        self.idx = Index()
        self.db = DB()
        self.lock = threading.Lock()
        self._enroll_cards()

    def _enroll_cards(self) -> None:
        for lid, l in self.idx.lessons.items():
            if lid in self.db.lessons_read():
                for c in l.cards:
                    self.db.srs_enroll(f"card:{c['id']}", "card")

    # ---- views
    def curriculum(self) -> dict:
        read, passed = self.db.lessons_read(), self.db.exercises_passed()
        mods = []
        for m in self.idx.modules:
            ls = []
            for l in m.lessons:
                ex_done = sum(e.id in passed for e in l.exercises)
                ls.append({"id": l.id, "title": l.title, "minutes": l.minutes, "read": l.id in read,
                           "exercises": len(l.exercises), "exercises_done": ex_done,
                           "done": l.id in read and ex_done == len(l.exercises)})
            mods.append({"id": m.id, "title": m.title, "summary": m.summary, "stage": m.stage, "lessons": ls})
        return {"modules": mods, "streak": self.db.streak(), **self.db.srs_counts()}

    def lesson(self, lid: str) -> dict:
        l = self.idx.lessons[lid]
        passed = self.db.exercises_passed()
        order = self.idx.lesson_order
        i = order.index(lid)
        return {"id": lid, "title": l.title, "minutes": l.minutes, "body": l.body,
                "prev": order[i - 1] if i else None, "next": order[i + 1] if i + 1 < len(order) else None,
                "cards": len(l.cards),
                "exercises": [{"id": e.id, "title": e.title, "difficulty": e.difficulty,
                               "passed": e.id in passed} for e in l.exercises]}

    def exercise(self, eid: str) -> dict:
        e = self.idx.exercises[eid]
        st = self.db.ex(eid)
        saved = json.loads(st["saved_files"]) if st["saved_files"] else None
        return {"id": eid, "title": e.title, "difficulty": e.difficulty, "prompt": e.prompt,
                "main": e.main, "mode": e.mode, "files": saved or e.starter(), "starter": e.starter(),
                "n_hints": len(e.hints), "hints_used": st["hints_used"], "passed": bool(st["passed_at"]),
                "lesson": e.lesson_id}

    def card(self, item: str) -> dict:
        l, c = self.idx.cards[item.split(":", 1)[1]]
        return {"item": item, "lesson": l.id, "lesson_title": l.title, "q": c["q"], "a": c["a"]}

    def today(self) -> dict:
        due_cards = [self.card(i) for i in self.db.srs_due("card", 12)
                     if i.split(":", 1)[1] in self.idx.cards]
        due_ex = [i[3:] for i in self.db.srs_due("ex", 2) if i[3:] in self.idx.exercises]
        read = self.db.lessons_read()
        nxt = next((lid for lid in self.idx.lesson_order if lid not in read), None)
        resume = None
        passed = self.db.exercises_passed()
        for lid in self.idx.lesson_order:
            l = self.idx.lessons[lid]
            if lid in read and any(e.id not in passed for e in l.exercises):
                resume = lid
                break
        return {"cards": due_cards,
                "redo": [{"id": e, "title": self.idx.exercises[e].title} for e in due_ex],
                "next_lesson": nxt, "next_title": self.idx.lessons[nxt].title if nxt else None,
                "resume_lesson": resume, "streak": self.db.streak(), **self.db.srs_counts(),
                "activity": self.db.activity_last()}

    def reference_list(self) -> list[dict]:
        out = []
        for p in sorted((CONTENT_DIR / "reference").glob("*.md")):
            first = p.read_text().splitlines()[0].lstrip("# ").strip()
            out.append({"id": p.stem, "title": first})
        return out

    def reference_get(self, name: str) -> dict:
        p = CONTENT_DIR / "reference" / f"{Path(name).name}.md"
        if not p.is_file():
            raise KeyError(name)
        return {"id": p.stem, "body": p.read_text()}

    # ---- actions
    def read_lesson(self, lid: str) -> None:
        self.db.mark_read(lid)
        for c in self.idx.lessons[lid].cards:
            self.db.srs_enroll(f"card:{c['id']}", "card", first_due_days=0)

    def run_check(self, eid: str, files: dict, redo: bool = False) -> dict:
        e = self.idx.exercises[eid]
        self.db.save_files(eid, files) if not redo else None
        if e.mode == "run":
            res = runner.run_main({**e.tests(), **files}, e.main, e.timeout)
            res["passed"] = res["ok"]
        else:
            res = runner.check(files, e.tests(), e.timeout)
        self.db.record_attempt(eid, res["passed"])
        if res["passed"]:
            first = self.db.srs_get(f"ex:{eid}") is None
            if first:
                self.db.srs_enroll(f"ex:{eid}", "ex", first_due_days=REDO_STEPS[0])
            elif redo:
                self.db.srs_grade(f"ex:{eid}", "good")
        elif redo:
            self.db.srs_grade(f"ex:{eid}", "again")
        return res

    def hint(self, eid: str, n: int) -> dict:
        e = self.idx.exercises[eid]
        n = max(0, min(n, len(e.hints) - 1))
        if e.hints:
            self.db.add_hint(eid)
        return {"hint": e.hints[n] if e.hints else "No hints for this one.", "n": n}

    def solution(self, eid: str) -> dict:
        self.db.mark_solution_seen(eid)
        return {"files": self.idx.exercises[eid].reference()}

    def reset(self, eid: str) -> dict:
        self.db.x("UPDATE exercise_progress SET saved_files=NULL WHERE exercise_id=?", eid)
        return {"files": self.idx.exercises[eid].starter()}


