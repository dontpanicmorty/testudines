import subprocess
import sys


def run(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, timeout=20)


def test_import_is_silent():
    r = run("-c", "import solution")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "", f"importing solution printed {r.stdout!r}; it should print nothing"


def test_script_still_prints():
    r = run("solution.py")
    assert r.stdout == "3 rows, total 60\n", f"running the script printed {r.stdout!r}"


def test_summarize():
    from solution import summarize

    assert summarize([1, 2]) == "2 rows, total 3"
    assert summarize([]) == "0 rows, total 0"
