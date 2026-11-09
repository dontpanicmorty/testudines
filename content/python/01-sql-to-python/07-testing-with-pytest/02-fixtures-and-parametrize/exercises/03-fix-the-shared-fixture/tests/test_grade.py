import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent

REVERSE = "def pytest_collection_modifyitems(items):\n    items.reverse()\n"


def run(reverse):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("PYTHON", "PYTEST"))}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory() as t:
        work = Path(t)
        shutil.copy(HERE / "my_tests.py", work / "my_tests.py")
        shutil.copy(HERE / "impl_good.py", work / "cart.py")
        if reverse:
            (work / "conftest.py").write_text(REVERSE)
        return subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--tb=short", "-p", "no:cacheprovider",
             "--disable-warnings", "my_tests.py"],
            cwd=work, env=env, capture_output=True, text=True, timeout=60,
        )


def test_passes_in_file_order():
    p = run(False)
    assert p.returncode == 0, "Tests fail when run in file order:\n" + p.stdout[-1200:]


def test_passes_in_reverse_order():
    p = run(True)
    assert p.returncode == 0, "Tests fail when run in reverse order:\n" + p.stdout[-1200:]


def test_all_four_tests_kept():
    p = run(False)
    m = re.search(r"(\d+) passed", p.stdout)
    assert m and int(m.group(1)) >= 4, "Keep all four tests."
