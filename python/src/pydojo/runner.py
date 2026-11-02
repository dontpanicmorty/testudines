"""Runs learner code in a throwaway directory using the interpreter running the app."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .paths import DATASETS_DIR

MAX_OUT = 20_000


def _env(workdir: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env.update(DOJO_DATA=str(DATASETS_DIR), PYTHONDONTWRITEBYTECODE="1",
               PYTHONUNBUFFERED="1", PYTHONIOENCODING="utf-8", NO_COLOR="1")
    return env


def _write(workdir: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        p = (workdir / name).resolve()
        if workdir.resolve() not in p.parents:
            raise ValueError(f"bad path: {name}")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


def _exec(args: list[str], cwd: Path, timeout: int) -> tuple[int, str]:
    try:
        r = subprocess.run([sys.executable, *args], cwd=cwd, env=_env(cwd), capture_output=True,
                           text=True, timeout=timeout, stdin=subprocess.DEVNULL)
        out = (r.stdout or "") + (r.stderr or "")
        code = r.returncode
    except subprocess.TimeoutExpired as e:
        out = ((e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""))
        out += f"\n[stopped: exceeded {timeout}s. Infinite loop?]"
        code = 124
    if len(out) > MAX_OUT:
        out = out[:MAX_OUT] + "\n[output truncated]"
    return code, out


def run_main(files: dict[str, str], main: str, timeout: int = 20) -> dict:
    with tempfile.TemporaryDirectory(prefix="dojo_") as t:
        wd = Path(t)
        _write(wd, files)
        code, out = _exec([main], wd, timeout)
    return {"ok": code == 0, "output": out}


def run_scratch(code: str, timeout: int = 20) -> dict:
    return run_main({"scratch.py": code}, "scratch.py", timeout)


def check(files: dict[str, str], tests: dict[str, str], timeout: int = 20) -> dict:
    with tempfile.TemporaryDirectory(prefix="dojo_") as t:
        wd = Path(t)
        _write(wd, files)
        _write(wd, tests)
        code, out = _exec(["-m", "pytest", "-q", "--tb=short", "-p", "no:cacheprovider",
                           "--disable-warnings", "-W", "ignore"], wd, timeout)
    m = re.search(r"(\d+) passed", out)
    f = re.search(r"(\d+) (failed|error)", out)
    return {"passed": code == 0, "output": out,
            "n_passed": int(m.group(1)) if m else 0, "n_failed": int(f.group(1)) if f else 0}
