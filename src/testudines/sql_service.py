"""The SQL section's service layer: the guided track, Practice Sessions, the Randomizer, grading and progress.

Carried over from SQL Dojo, which this section replaces:
- The guided track is the 100 track exercises in order; Practice Sessions and the Randomizer draw on all
  300 (track + practice families). A Practice Session takes the first N exercises of the chosen
  difficulties, in curriculum order; the Randomizer takes N at random and hides their difficulty.
- An exercise's query is saved as you type; a check that fails counts toward unlocking the solution,
  which is offered after FAIL_THRESHOLD failed checks.
- If an exercise's reference solution has changed since you worked on it, your old progress on it is
  dropped (it may be a different exercise now), as SQL Dojo did.
- Export/Import use SQL Dojo's file format, so a SQL Dojo export can be imported here.
"""
from __future__ import annotations

import random
from datetime import datetime

from . import sql_grader
from .db import DB
from .sql_content import DIFFICULTIES, SqlExercise, SqlIndex

FAIL_THRESHOLD = 3
MODES = ("track", "practice", "randomizer")


class SqlService:
    def __init__(self, db: DB, idx: SqlIndex | None = None) -> None:
        self.idx = idx or SqlIndex()
        self.db = db

    # ---- progress
    def _fingerprint(self, e: SqlExercise) -> str:
        return e.solution.strip()

    def state(self, eid: str) -> dict:
        """This user's progress on one exercise, dropped first if the exercise has changed since."""
        e = self.idx.by_id[eid]
        st = self.db.sql_get(eid)
        if st["fingerprint"] is not None and st["fingerprint"] != self._fingerprint(e):
            self.db.sql_put(eid, completed_at=None, code=None, fail_count=0)
            st = self.db.sql_get(eid)
        if st["fingerprint"] != self._fingerprint(e):
            self.db.sql_put(eid, fingerprint=self._fingerprint(e))
        return st

    def completed(self) -> set[str]:
        return self.db.sql_completed()

    def track_done(self) -> tuple[int, int]:
        done = self.completed()
        return sum(e.id in done for e in self.idx.track), len(self.idx.track)

    def exercise(self, eid: str) -> dict:
        e = self.idx.by_id[eid]
        st = self.state(eid)
        return {"id": eid, "title": e.title, "difficulty": e.difficulty, "concept": e.concept,
                "tables": e.tables, "prompt": e.prompt, "hint": e.hint, "group": e.group_title,
                "track": e.track, "code": st["code"] if st["code"] is not None else e.starter,
                "completed": st["completed_at"] is not None, "fail_count": st["fail_count"],
                "solution_available": st["completed_at"] is not None or st["fail_count"] >= FAIL_THRESHOLD}

    def sample_tables(self, eid: str) -> list[dict]:
        return sql_grader.sample_tables(self.idx.by_id[eid].schema)

    # ---- actions
    def save_code(self, eid: str, code: str) -> None:
        self.state(eid)
        self.db.sql_put(eid, code=code)

    def run(self, eid: str, code: str) -> sql_grader.Result:
        return sql_grader.run(self.idx.by_id[eid].schema, code)

    def check(self, eid: str, code: str) -> dict:
        e = self.idx.by_id[eid]
        st = self.state(eid)
        res = sql_grader.check(e.schema, e.solution, code)
        if res["passed"]:
            self.db.sql_put(eid, code=code, fail_count=0,
                            completed_at=st["completed_at"] or datetime.now().isoformat())
            self.db.bump("sql")
        else:
            fails = (st["fail_count"] or 0) + 1
            self.db.sql_put(eid, code=code, fail_count=fails)
            if fails >= FAIL_THRESHOLD and not res["error"]:
                res["message"] += ' Stuck? "Show solution" is now available.'
        res["solution_available"] = res["passed"] or self.db.sql_get(eid)["fail_count"] >= FAIL_THRESHOLD \
            or self.db.sql_get(eid)["completed_at"] is not None
        return res

    def solution(self, eid: str) -> str:
        return self.idx.by_id[eid].solution

    def reset(self, eid: str) -> str:
        e = self.idx.by_id[eid]
        self.db.sql_put(eid, code=e.starter)
        return e.starter

    # ---- queues: the guided track, a Practice Session, the Randomizer
    def pool(self, difficulties: list[str]) -> list[SqlExercise]:
        return [e for e in self.idx.all if e.difficulty in difficulties]

    def start(self, mode: str, difficulties: list[str] | None = None, count: int | None = None) -> dict:
        """A new queue for a mode, saved so it can be resumed: {mode, queue, current}."""
        if mode == "track":
            queue = [e.id for e in self.idx.track]
            current = self.db.state_get("last_track") or queue[0]
        elif mode == "practice":
            chosen = DIFFICULTIES if difficulties is None else difficulties  # none given: all; none ticked: none
            diffs = [d for d in chosen if d in DIFFICULTIES]
            pool = self.pool(diffs)
            if not pool:
                raise ValueError("No exercises match that selection.")
            n = max(1, min(len(pool), count or len(pool)))
            queue = [e.id for e in pool[:n]]
            current = queue[0]
        elif mode == "randomizer":
            n = max(1, min(len(self.idx.all), count or 10))
            queue = [e.id for e in random.sample(self.idx.all, n)]
            current = queue[0]
        else:
            raise ValueError(mode)
        session = {"mode": mode, "queue": queue, "current": current}
        if mode != "track":
            self.db.state_set(f"saved_{mode}", session)
        return session

    def saved(self, mode: str) -> dict | None:
        """A saved Practice Session or Randomizer, if it still fits the curriculum."""
        s = self.db.state_get(f"saved_{mode}")
        if not s or not s.get("queue"):
            return None
        queue = [i for i in s["queue"] if i in self.idx.by_id]
        if not queue:
            return None
        return {"mode": mode, "queue": queue, "current": s["current"] if s.get("current") in queue else queue[0]}

    def remember(self, session: dict, current: str) -> None:
        session["current"] = current
        if session["mode"] == "track":
            self.db.state_set("last_track", current)
        else:
            self.db.state_set(f"saved_{session['mode']}", session)

    def end(self, mode: str) -> None:
        if mode != "track":
            self.db.state_set(f"saved_{mode}", None)

    # ---- settings
    def setting(self, key: str, default=None):
        return self.db.state_get(f"setting_{key}", default)

    def set_setting(self, key: str, value) -> None:
        self.db.state_set(f"setting_{key}", value)

    # ---- export / import (SQL Dojo's format: {exercise id: {completed, code, failCount, contentFingerprint}})
    def export(self) -> dict:
        out = {}
        for eid, st in self.db.sql_all().items():
            out[eid] = {"completed": st["completed_at"] is not None, "code": st["code"] or "",
                        "failCount": st["fail_count"] or 0, "contentFingerprint": st["fingerprint"]}
        return out

    def import_progress(self, data: dict) -> int:
        """Replace this user's SQL progress with an export (from Testudines or SQL Dojo). Returns how many
        exercises it brought back. Exercises that no longer exist are skipped; one whose solution has
        changed since the export keeps its query but not its completion."""
        if not isinstance(data, dict):
            raise ValueError("That file isn't a progress export.")
        entries = {k: v for k, v in data.items() if isinstance(v, dict)}
        if data and not entries:
            raise ValueError("That file isn't a progress export.")
        self.db.sql_clear()
        n = 0
        now = datetime.now().isoformat()
        for eid, st in entries.items():
            e = self.idx.by_id.get(eid)
            if e is None:
                continue
            fp = (st.get("contentFingerprint") or "").strip()
            same = not fp or fp == self._fingerprint(e)
            self.db.sql_put(eid, code=st.get("code") or None, fail_count=int(st.get("failCount") or 0),
                            completed_at=now if (st.get("completed") and same) else None,
                            fingerprint=self._fingerprint(e))
            n += 1
        return n
