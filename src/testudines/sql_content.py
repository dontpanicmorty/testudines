"""Loads the SQL curriculum from content/sql/.

content/sql/track/<NN-lesson>/lesson.toml          id, number, title, difficulty
content/sql/track/<NN-lesson>/schema.sql           tables shared by the lesson's exercises (optional)
content/sql/practice/<NN-family>/family.toml       id, title, source_prompt
content/sql/practice/<NN-family>/schema.sql        tables shared by the family's exercises
content/sql/.../exercises/<NN-exercise>/
    exercise.toml   id, title, difficulty (easy | medium | hard), concept, tables, hint
    prompt.md       what to write a query for (markdown)
    solution.sql    the reference answer; a learner's result must match its result
    starter.sql     what the editor starts with
    schema.sql      the exercise's own tables, when it doesn't use the lesson's or family's

The guided track is the track lessons in folder order; practice families are extra exercises drawn on by
Practice Sessions and the Randomizer along with the track. Like the Python curriculum, each exercise's
permanent `id` is its identity (progress is keyed by it); folder names only set the order.
"""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .paths import SQL_CONTENT_DIR

DIFFICULTIES = ("easy", "medium", "hard")


@dataclass
class SqlExercise:
    id: str
    dir: Path
    title: str
    difficulty: str
    concept: str
    tables: str
    hint: str
    prompt: str
    schema: str
    solution: str
    starter: str
    group_id: str      # the lesson or family it belongs to
    group_title: str
    track: bool        # part of the guided track (else a practice family's exercise)


@dataclass
class SqlGroup:
    id: str
    dir: Path
    title: str
    difficulty: str
    track: bool
    exercises: list[SqlExercise] = field(default_factory=list)


def _read(p: Path) -> str:
    return p.read_text() if p.is_file() else ""


def _load_group(d: Path, meta_name: str, track: bool) -> SqlGroup:
    meta = tomllib.loads((d / meta_name).read_text())
    group = SqlGroup(meta.get("id", ""), d, meta.get("title", d.name), meta.get("difficulty", ""), track)
    shared = _read(d / "schema.sql")
    root = d / "exercises"
    for ed in sorted(p for p in root.iterdir() if p.is_dir()) if root.is_dir() else []:
        em = tomllib.loads((ed / "exercise.toml").read_text())
        group.exercises.append(SqlExercise(
            id=em.get("id", ""), dir=ed, title=em.get("title", ed.name), difficulty=em.get("difficulty", "easy"),
            concept=em.get("concept", ""), tables=em.get("tables", ""), hint=em.get("hint", ""),
            prompt=_read(ed / "prompt.md"), schema=_read(ed / "schema.sql") or shared,
            solution=_read(ed / "solution.sql"), starter=_read(ed / "starter.sql"),
            group_id=group.id, group_title=group.title, track=track))
    return group


def load_sql(root: Path = SQL_CONTENT_DIR) -> tuple[list[SqlGroup], list[SqlGroup]]:
    """(track lessons, practice families), each in folder order."""
    def groups(sub: str, meta: str, track: bool) -> list[SqlGroup]:
        base = root / sub
        if not base.is_dir():
            return []
        return [_load_group(d, meta, track) for d in sorted(base.iterdir()) if (d / meta).is_file()]
    return groups("track", "lesson.toml", True), groups("practice", "family.toml", False)


def sql_id_problems(lessons: list[SqlGroup], families: list[SqlGroup]) -> list[str]:
    out, seen = [], {}
    for g in lessons + families:
        for e in g.exercises:
            where = f"{g.dir.name}/{e.dir.name}"
            if not e.id:
                out.append(f"MISSING exercise id: {where}")
            elif e.id in seen:
                out.append(f"DUPLICATE id {e.id!r}: {where} and {seen[e.id]}")
            else:
                seen[e.id] = where
            if e.difficulty not in DIFFICULTIES:
                out.append(f"BAD difficulty {e.difficulty!r}: {where}")
    return out


class SqlIndex:
    def __init__(self, root: Path = SQL_CONTENT_DIR) -> None:
        self.lessons, self.families = load_sql(root)
        problems = sql_id_problems(self.lessons, self.families)
        if problems:
            raise ValueError("SQL content problems:\n  " + "\n  ".join(problems))
        self.track = [e for g in self.lessons for e in g.exercises]       # the guided track, in order
        self.extra = [e for g in self.families for e in g.exercises]
        self.all = self.track + self.extra                                   # every exercise
        self.by_id = {e.id: e for e in self.all}
