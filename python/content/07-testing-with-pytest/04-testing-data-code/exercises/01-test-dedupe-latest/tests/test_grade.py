"""Grades learner-written tests: they must pass on the correct implementation and
fail on every deliberately buggy implementation shipped next to this file."""
import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

HERE = Path(__file__).parent
MODULE = "dedupe"
FILES = "my_tests.py".split(",")
REQUIRE = [r for r in "".split(",") if r]
MIN_TESTS = 5


def run_learner_tests(impl):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("PYTHON", "DOJO_", "PYTEST"))}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory() as t:
        work = Path(t)
        for name in FILES:
            shutil.copy(HERE / name, work / name)
        shutil.copy(HERE / impl, work / f"{MODULE}.py")
        return subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--tb=short", "-p", "no:cacheprovider",
             "--disable-warnings", FILES[0]],
            cwd=work, env=env, capture_output=True, text=True, timeout=60,
        )


def tail(p):
    return (p.stdout + p.stderr)[-1500:]


def describe(path):
    doc = ast.get_docstring(ast.parse((HERE / path).read_text())) or path
    return doc.strip().splitlines()[0]


BUGS = sorted(p.name for p in HERE.glob("impl_bug_*.py"))


def test_your_tests_pass_on_the_correct_implementation():
    p = run_learner_tests("impl_good.py")
    assert p.returncode == 0, "Your tests must pass against the correct implementation. Output:\n" + tail(p)
    m = re.search(r"(\d+) passed", p.stdout)
    n = int(m.group(1)) if m else 0
    assert n >= MIN_TESTS, f"Write at least {MIN_TESTS} test cases (found {n})."


@pytest.mark.parametrize("needle", REQUIRE)
def test_uses_required_feature(needle):
    src = (HERE / FILES[0]).read_text()
    assert needle in src, f"This exercise asks you to use `{needle}` in your tests."


@pytest.mark.parametrize("impl", BUGS, ids=[describe(b) for b in BUGS])
def test_catches_bug(impl):
    p = run_learner_tests(impl)
    assert p.returncode != 0, (
        f"Your tests still pass on a buggy version: {describe(impl)}. "
        "Add a test that would fail on it."
    )
    assert p.returncode == 1, "Your test file errored instead of failing:\n" + tail(p)
