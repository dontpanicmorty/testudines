"""Curriculum QA for both sections. Run it after adding or changing content: `testudines validate`.

Python: every exercise's starter must FAIL its tests and its reference must PASS.
SQL: every field must be filled in, every exercise's tables must load, its solution must run, and its starter
must not already pass.
A solution that returns no rows is listed as a note, not a problem: some exercises expect an empty result
("users with no friends at all" when everyone has one), and some build tables rather than query them.
In both sections, every id must be present and unique.
"""
from __future__ import annotations

import sys

from . import runner, sql_grader
from .content import id_problems, load_curriculum
from .sql_content import load_sql, sql_id_problems


def check_python(only: str | None = None) -> int:
    bad = 0
    mods = load_curriculum()
    for msg in id_problems(mods):
        print(msg); bad += 1
    if only:  # check just the modules of one path (or module) whose id or folder name contains this
        mods = [m for m in mods if only in m.path or only in m.id]
    n = 0
    for m in mods:
        for l in m.lessons:
            if not l.body.strip():
                print(f"EMPTY LESSON {l.id}"); bad += 1
            for i, c in enumerate(l.cards):
                if not c.get("q") or not c.get("a"):
                    print(f"BAD CARD {l.id}#{i}"); bad += 1
            for e in l.exercises:
                n += 1
                ref, tests = e.reference(), e.tests()
                if not ref or not tests:
                    print(f"MISSING reference/tests: {e.id}"); bad += 1; continue
                if e.mode == "run":
                    r = runner.run_main({**tests, **ref}, e.main, e.timeout, e.memory_mb or None)
                    ok_ref = r["ok"]
                    ok_start = False
                else:
                    ok_ref = runner.check(ref, tests, e.timeout, e.memory_mb or None)["passed"]
                    ok_start = runner.check(e.starter(), tests, e.timeout, e.memory_mb or None)["passed"]
                if not ok_ref:
                    print(f"REFERENCE FAILS: {e.id}"); bad += 1
                if ok_start:
                    print(f"STARTER ALREADY PASSES: {e.id}"); bad += 1
    print(f"Python: {len(mods)} modules, {sum(len(m.lessons) for m in mods)} lessons, {n} exercises, {bad} problems")
    return bad


def check_sql() -> int:
    bad = notes = 0
    lessons, families = load_sql()
    for msg in sql_id_problems(lessons, families):
        print(msg); bad += 1
    n = 0
    for g in lessons + families:
        if not g.exercises:
            print(f"NO EXERCISES: {g.dir.name}"); bad += 1
        for e in g.exercises:
            n += 1
            where = f"{g.dir.name}/{e.dir.name} ({e.id})"
            for name, text in (("prompt.md", e.prompt), ("solution.sql", e.solution), ("schema.sql", e.schema),
                               ("starter.sql", e.starter), ("title", e.title), ("concept", e.concept),
                               ("tables", e.tables), ("hint", e.hint)):
                if not (text or "").strip():
                    print(f"MISSING {name}: {where}"); bad += 1
            if not sql_grader.sample_tables(e.schema):
                print(f"NO TABLES (schema.sql creates none, or fails): {where}"); bad += 1
            ref = sql_grader.run(e.schema, e.solution)
            if ref.error:
                print(f"SOLUTION FAILS: {where}: {ref.error}"); bad += 1
            elif not ref.rows:
                print(f"note: solution returns no rows (an empty result or table-building exercise): {where}")
                notes += 1
            if sql_grader.check(e.schema, e.solution, e.starter)["passed"]:
                print(f"STARTER ALREADY PASSES: {where}"); bad += 1
    print(f"SQL: {len(lessons)} track lessons, {len(families)} practice families, {n} exercises, {bad} problems"
          + (f" ({notes} notes)" if notes else ""))
    return bad


def main(section: str | None = None, only: str | None = None) -> int:
    bad = 0
    if section in (None, "sql"):
        bad += check_sql()
    if section in (None, "python"):
        bad += check_python(only)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
