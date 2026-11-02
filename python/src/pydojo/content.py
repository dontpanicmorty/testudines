"""Loads the curriculum from the content/ folder.

content/<NN-module>/module.toml
content/<NN-module>/<NN-lesson>/lesson.md        (+++ toml front matter incl. permanent id +++, markdown)
content/<NN-module>/<NN-lesson>/cards.toml       ([[card]] id = "", q = "", a = "")

Identity vs order: every lesson, exercise and card has a permanent `id` stored in its own file.
Progress is keyed by id only. Folder names and card positions control ORDER, never identity,
so renaming, reordering or inserting content never disturbs a learner's progress.
content/<NN-module>/<NN-lesson>/exercises/<NN-ex>/
    exercise.toml  prompt.md  starter/  reference/  tests/
"""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .paths import CONTENT_DIR


def _read_files(d: Path) -> dict[str, str]:
    if not d.is_dir():
        return {}
    return {p.relative_to(d).as_posix(): p.read_text() for p in sorted(d.rglob("*")) if p.is_file()}


def _split_front_matter(text: str) -> tuple[dict, str]:
    if text.startswith("+++"):
        _, fm, body = text.split("+++", 2)
        return tomllib.loads(fm), body.lstrip("\n")
    return {}, text


@dataclass
class Exercise:
    id: str
    lesson_id: str
    dir: Path
    title: str
    difficulty: int
    main: str
    hints: list[str]
    prompt: str
    mode: str  # "tests" (pytest) or "run" (just execute)
    timeout: int

    def starter(self) -> dict[str, str]:
        return _read_files(self.dir / "starter")

    def reference(self) -> dict[str, str]:
        return _read_files(self.dir / "reference")

    def tests(self) -> dict[str, str]:
        return _read_files(self.dir / "tests")


@dataclass
class Lesson:
    id: str
    dir: Path
    title: str
    minutes: int
    body: str
    cards: list[dict]
    exercises: list[Exercise] = field(default_factory=list)


@dataclass
class Module:
    id: str
    title: str
    summary: str
    stage: str
    lessons: list[Lesson] = field(default_factory=list)


def _load_exercise(lesson_id: str, d: Path) -> Exercise:
    meta = tomllib.loads((d / "exercise.toml").read_text())
    return Exercise(
        id=meta.get("id", ""), lesson_id=lesson_id, dir=d, title=meta["title"],
        difficulty=meta.get("difficulty", 1), main=meta.get("main", "solution.py"),
        hints=meta.get("hints", []), prompt=(d / "prompt.md").read_text(),
        mode=meta.get("mode", "tests"), timeout=meta.get("timeout", 20),
    )


def load_curriculum(root: Path = CONTENT_DIR) -> list[Module]:
    modules: list[Module] = []
    for md in sorted(p for p in root.iterdir() if p.is_dir() and (p / "module.toml").exists()):
        meta = tomllib.loads((md / "module.toml").read_text())
        mod = Module(md.name, meta["title"], meta.get("summary", ""), meta.get("stage", ""))
        for ld in sorted(p for p in md.iterdir() if p.is_dir() and (p / "lesson.md").exists()):
            fm, body = _split_front_matter((ld / "lesson.md").read_text())
            lid = fm.get("id", "")
            cards_f = ld / "cards.toml"
            cards = tomllib.loads(cards_f.read_text()).get("card", []) if cards_f.exists() else []
            lesson = Lesson(lid, ld, fm.get("title", ld.name), fm.get("minutes", 20), body, cards)
            ex_root = ld / "exercises"
            if ex_root.is_dir():
                lesson.exercises = [_load_exercise(lid, e) for e in sorted(ex_root.iterdir()) if e.is_dir()]
            mod.lessons.append(lesson)
        modules.append(mod)
    return modules


def id_problems(modules: list[Module]) -> list[str]:
    """Every lesson/exercise/card needs a unique, non-empty permanent id."""
    out: list[str] = []
    seen: dict[str, str] = {}

    def claim(kind: str, ident: str, where: str) -> None:
        if not ident:
            out.append(f"MISSING {kind} id: {where}")
        elif ident in seen:
            out.append(f"DUPLICATE id {ident!r}: {where} and {seen[ident]}")
        else:
            seen[ident] = where

    for m in modules:
        for l in m.lessons:
            claim("lesson", l.id, l.dir.name)
            for i, c in enumerate(l.cards):
                claim("card", c.get("id", ""), f"{l.dir.name} card #{i + 1}")
            for e in l.exercises:
                claim("exercise", e.id, f"{l.dir.name}/{e.dir.name}")
    return out


class Index:
    """Cached lookup by permanent id. Order comes from folder order only."""

    def __init__(self) -> None:
        self.reload()

    def reload(self) -> None:
        self.modules = load_curriculum()
        problems = id_problems(self.modules)
        if problems:
            raise ValueError("Content id problems:\n  " + "\n  ".join(problems))
        self.lessons = {l.id: l for m in self.modules for l in m.lessons}
        self.exercises = {e.id: e for l in self.lessons.values() for e in l.exercises}
        self.cards = {c["id"]: (l, c) for l in self.lessons.values() for c in l.cards}
        self.lesson_order = [l.id for m in self.modules for l in m.lessons]
