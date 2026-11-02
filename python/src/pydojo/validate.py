"""Content QA: every exercise's starter must FAIL its tests and its reference must PASS."""
from __future__ import annotations

import sys

from . import runner
from .content import id_problems, load_curriculum


def main() -> int:
    bad = 0
    mods = load_curriculum()
    for msg in id_problems(mods):
        print(msg); bad += 1
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
                    r = runner.run_main({**tests, **ref}, e.main, e.timeout)
                    ok_ref = r["ok"]
                    ok_start = False
                else:
                    ok_ref = runner.check(ref, tests, e.timeout)["passed"]
                    ok_start = runner.check(e.starter(), tests, e.timeout)["passed"]
                if not ok_ref:
                    print(f"REFERENCE FAILS: {e.id}"); bad += 1
                if ok_start:
                    print(f"STARTER ALREADY PASSES: {e.id}"); bad += 1
    print(f"{len(mods)} modules, {sum(len(m.lessons) for m in mods)} lessons, {n} exercises, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
