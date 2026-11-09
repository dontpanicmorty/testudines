"""A user's progress in both sections, stored in one SQLite file in that user's folder (see users.py).

Python: lessons read, exercises passed, spaced repetition and activity, as in Py Dojo.
SQL: each exercise's saved query, whether it's solved and how many checks failed, plus the saved
Practice Session and Randomizer queues, so leaving and coming back resumes where you were."""
from __future__ import annotations

import json
import sqlite3
import threading
from datetime import date, datetime, timedelta

from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS lesson_progress(lesson_id TEXT PRIMARY KEY, read_at TEXT);
CREATE TABLE IF NOT EXISTS exercise_progress(
  exercise_id TEXT PRIMARY KEY, passed_at TEXT, attempts INTEGER DEFAULT 0,
  hints_used INTEGER DEFAULT 0, solution_seen INTEGER DEFAULT 0, saved_files TEXT);
CREATE TABLE IF NOT EXISTS srs(
  item TEXT PRIMARY KEY, kind TEXT, due TEXT, interval REAL DEFAULT 0,
  ease REAL DEFAULT 2.5, reps INTEGER DEFAULT 0, lapses INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS activity(day TEXT, kind TEXT, n INTEGER DEFAULT 0, PRIMARY KEY(day, kind));
CREATE TABLE IF NOT EXISTS sql_progress(
  exercise_id TEXT PRIMARY KEY, completed_at TEXT, code TEXT, fail_count INTEGER DEFAULT 0, fingerprint TEXT);
CREATE TABLE IF NOT EXISTS sql_state(key TEXT PRIMARY KEY, value TEXT);
"""


def today() -> str:
    return date.today().isoformat()


class DB:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.c = sqlite3.connect(path, check_same_thread=False)
        self.c.row_factory = sqlite3.Row
        self.c.executescript(SCHEMA)

    def q(self, sql: str, *a) -> list[sqlite3.Row]:
        with self.lock:
            return self.c.execute(sql, a).fetchall()

    def x(self, sql: str, *a) -> None:
        with self.lock:
            self.c.execute(sql, a)
            self.c.commit()

    # --- activity / streak
    def bump(self, kind: str) -> None:
        self.x("INSERT INTO activity VALUES(?,?,1) ON CONFLICT(day,kind) DO UPDATE SET n=n+1", today(), kind)

    def streak(self) -> int:
        days = {r["day"] for r in self.q("SELECT DISTINCT day FROM activity")}
        d, n = date.today(), 0
        if d.isoformat() not in days:
            d -= timedelta(days=1)
        while d.isoformat() in days:
            n += 1
            d -= timedelta(days=1)
        return n

    # --- lessons
    def mark_read(self, lid: str) -> None:
        self.x("INSERT OR IGNORE INTO lesson_progress VALUES(?,?)", lid, datetime.now().isoformat())
        self.bump("lesson")

    def lessons_read(self) -> set[str]:
        return {r["lesson_id"] for r in self.q("SELECT lesson_id FROM lesson_progress")}

    # --- exercises
    def ex(self, eid: str) -> dict:
        r = self.q("SELECT * FROM exercise_progress WHERE exercise_id=?", eid)
        return dict(r[0]) if r else {"exercise_id": eid, "passed_at": None, "attempts": 0,
                                     "hints_used": 0, "solution_seen": 0, "saved_files": None}

    def ex_touch(self, eid: str) -> None:
        self.x("INSERT OR IGNORE INTO exercise_progress(exercise_id) VALUES(?)", eid)

    def save_files(self, eid: str, files: dict) -> None:
        self.ex_touch(eid)
        self.x("UPDATE exercise_progress SET saved_files=? WHERE exercise_id=?", json.dumps(files), eid)

    def record_attempt(self, eid: str, passed: bool) -> None:
        self.ex_touch(eid)
        self.x("UPDATE exercise_progress SET attempts=attempts+1 WHERE exercise_id=?", eid)
        if passed:
            self.x("UPDATE exercise_progress SET passed_at=COALESCE(passed_at,?) WHERE exercise_id=?",
                   datetime.now().isoformat(), eid)
            self.bump("exercise")

    def add_hint(self, eid: str) -> None:
        self.ex_touch(eid)
        self.x("UPDATE exercise_progress SET hints_used=hints_used+1 WHERE exercise_id=?", eid)

    def mark_solution_seen(self, eid: str) -> None:
        self.ex_touch(eid)
        self.x("UPDATE exercise_progress SET solution_seen=1 WHERE exercise_id=?", eid)

    def exercises_passed(self) -> set[str]:
        return {r["exercise_id"] for r in self.q("SELECT exercise_id FROM exercise_progress WHERE passed_at IS NOT NULL")}

    # --- spaced repetition (SM-2 style)
    def srs_get(self, item: str) -> sqlite3.Row | None:
        r = self.q("SELECT * FROM srs WHERE item=?", item)
        return r[0] if r else None

    def srs_enroll(self, item: str, kind: str, first_due_days: float = 0) -> None:
        due = (date.today() + timedelta(days=first_due_days)).isoformat()
        self.x("INSERT OR IGNORE INTO srs(item,kind,due) VALUES(?,?,?)", item, kind, due)

    def srs_grade(self, item: str, grade: str) -> dict:
        """grade: again | hard | good | easy"""
        r = self.srs_get(item)
        if r is None:
            self.srs_enroll(item, item.split(":")[0])
            r = self.srs_get(item)
        ease, interval, reps, lapses = r["ease"], r["interval"], r["reps"], r["lapses"]
        if grade == "again":
            reps, lapses, interval, ease = 0, lapses + 1, 0, max(1.3, ease - 0.2)
            due = date.today() + timedelta(days=1)
        else:
            if reps == 0:
                interval = 1
            elif reps == 1:
                interval = 3
            else:
                interval = interval * ease * {"hard": 0.6, "good": 1.0, "easy": 1.4}[grade]
            ease = max(1.3, ease + {"hard": -0.15, "good": 0.0, "easy": 0.15}[grade])
            reps += 1
            due = date.today() + timedelta(days=max(1, round(interval)))
        self.x("UPDATE srs SET due=?,interval=?,ease=?,reps=?,lapses=? WHERE item=?",
               due.isoformat(), interval, ease, reps, lapses, item)
        self.bump("review")
        return {"due": due.isoformat(), "interval": interval}

    def srs_due(self, kind: str, limit: int) -> list[str]:
        rows = self.q("SELECT item FROM srs WHERE kind=? AND due<=? ORDER BY due, reps LIMIT ?",
                      kind, today(), limit)
        return [r["item"] for r in rows]

    def srs_counts(self) -> dict:
        t = today()
        return {
            "cards_total": self.q("SELECT COUNT(*) n FROM srs WHERE kind='card'")[0]["n"],
            "cards_due": self.q("SELECT COUNT(*) n FROM srs WHERE kind='card' AND due<=?", t)[0]["n"],
            "redo_due": self.q("SELECT COUNT(*) n FROM srs WHERE kind='ex' AND due<=?", t)[0]["n"],
        }

    def activity_last(self, days: int = 84) -> dict[str, int]:
        since = (date.today() - timedelta(days=days)).isoformat()
        out: dict[str, int] = {}
        for r in self.q("SELECT day, SUM(n) n FROM activity WHERE day>=? GROUP BY day", since):
            out[r["day"]] = r["n"]
        return out

    # --- SQL section
    def sql_get(self, eid: str) -> dict:
        r = self.q("SELECT * FROM sql_progress WHERE exercise_id=?", eid)
        return dict(r[0]) if r else {"exercise_id": eid, "completed_at": None, "code": None,
                                     "fail_count": 0, "fingerprint": None}

    def sql_put(self, eid: str, **fields) -> None:
        self.x("INSERT OR IGNORE INTO sql_progress(exercise_id) VALUES(?)", eid)
        for k, v in fields.items():
            assert k in ("completed_at", "code", "fail_count", "fingerprint"), k
            self.x(f"UPDATE sql_progress SET {k}=? WHERE exercise_id=?", v, eid)

    def sql_all(self) -> dict[str, dict]:
        return {r["exercise_id"]: dict(r) for r in self.q("SELECT * FROM sql_progress")}

    def sql_clear(self) -> None:
        self.x("DELETE FROM sql_progress")

    def sql_completed(self) -> set[str]:
        return {r["exercise_id"] for r in self.q("SELECT exercise_id FROM sql_progress WHERE completed_at IS NOT NULL")}

    def state_get(self, key: str, default=None):
        r = self.q("SELECT value FROM sql_state WHERE key=?", key)
        return json.loads(r[0]["value"]) if r else default

    def state_set(self, key: str, value) -> None:
        if value is None:
            self.x("DELETE FROM sql_state WHERE key=?", key)
        else:
            self.x("INSERT INTO sql_state VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                   key, json.dumps(value))
