"""Runs learner code in a throwaway directory using the interpreter running the app.

Learner code must never burden the machine, whatever it does: loop forever, print without end, grow a list
without end, or start other programs. So every run of learner code:
- has a time limit (the exercise's `timeout`, 20 seconds by default);
- has a memory limit (memory_limit_mb(): a share of this computer's memory, 512 MB to 1.5 GB, or the
  exercise's `memory_mb`). A watchdog enforces it on every system; on Windows a job object also caps it;
- is stopped once it prints more than MAX_STREAM bytes, and only its first MAX_OUT characters are kept;
- runs at a lower priority than the app, so the window stays responsive while it works;
- is stopped together with every process it started;
- waits its turn: at most MAX_PARALLEL learner programs run at once.
"""
from __future__ import annotations

import os
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import psutil

from .paths import DATASETS_DIR

MAX_OUT = 20_000          # characters of output kept and shown
MAX_STREAM = 1_000_000    # bytes of output after which a program is stopped
MAX_PARALLEL = 2          # learner programs running at once; more wait their turn
POLL = 0.05               # seconds between watchdog checks
_slots = threading.BoundedSemaphore(MAX_PARALLEL)
WINDOWS = sys.platform == "win32"


def memory_limit_mb() -> int:
    """How much memory one learner program may use: a sixth of this computer's memory, 512 MB to 1.5 GB.
    Enough for every exercise (the largest use about 200 MB), small enough for a 4 GB machine."""
    total_mb = psutil.virtual_memory().total // (1024 * 1024)
    return int(max(512, min(1536, total_mb // 6)))


def _env(workdir: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env.update(DOJO_DATA=str(DATASETS_DIR), PYTHONDONTWRITEBYTECODE="1",
               PYTHONUNBUFFERED="1", PYTHONIOENCODING="utf-8", NO_COLOR="1",
               # libraries that start a thread per CPU core (numpy, polars, pyarrow) use at most two
               OMP_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2", MKL_NUM_THREADS="2", POLARS_MAX_THREADS="2",
               RAYON_NUM_THREADS="2")
    return env


def _write(workdir: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        p = (workdir / name).resolve()
        if workdir.resolve() not in p.parents:
            raise ValueError(f"bad path: {name}")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


def _python() -> str:
    """The interpreter to run learner code with. On Windows the app runs under pythonw.exe (no console);
    learner code runs under the python.exe beside it, so its output can be captured."""
    exe = Path(sys.executable)
    if exe.name.lower() == "pythonw.exe" and (exe.parent / "python.exe").exists():
        return str(exe.parent / "python.exe")
    return sys.executable


def _windows_job(proc: subprocess.Popen, limit: int):
    """Windows only: put the program in a job object that caps its memory and, when closed, ends every
    process it started. Returns the job handle, or None if Windows refused (the watchdog still applies)."""
    try:
        import ctypes
        from ctypes import wintypes

        class IoCounters(ctypes.Structure):
            _fields_ = [(n, ctypes.c_ulonglong) for n in (
                "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

        class BasicLimits(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                        ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                        ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD),
                        ("SchedulingClass", wintypes.DWORD)]

        class ExtendedLimits(ctypes.Structure):
            _fields_ = [("BasicLimitInformation", BasicLimits), ("IoInfo", IoCounters),
                        ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                        ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]

        k = ctypes.WinDLL("kernel32", use_last_error=True)
        k.CreateJobObjectW.restype = wintypes.HANDLE
        k.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        job = k.CreateJobObjectW(None, None)
        if not job:
            return None
        info = ExtendedLimits()
        info.BasicLimitInformation.LimitFlags = 0x200 | 0x2000  # JOB_MEMORY | KILL_ON_JOB_CLOSE
        info.JobMemoryLimit = limit
        ok = k.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info))  # extended limits
        ok = ok and k.AssignProcessToJobObject(job, int(proc._handle))
        if not ok:
            k.CloseHandle(job)
            return None
        return (k, job)
    except Exception:
        return None


def _tree(ps: psutil.Process) -> list[psutil.Process]:
    try:
        return [ps, *ps.children(recursive=True)]
    except psutil.Error:
        return [ps]


def _memory(ps: psutil.Process) -> int:
    total = 0
    for p in _tree(ps):
        try:
            total += p.memory_info().rss
        except psutil.Error:
            pass
    return total


def _kill_tree(proc: subprocess.Popen, ps: psutil.Process | None) -> None:
    """Stop the program and everything it started."""
    procs = _tree(ps) if ps else []
    if not WINDOWS:
        try:
            os.killpg(proc.pid, signal.SIGKILL)  # its own process group (start_new_session)
        except OSError:
            pass
    for p in procs:
        try:
            p.kill()
        except psutil.Error:
            pass
    try:
        proc.kill()
    except OSError:
        pass
    psutil.wait_procs(procs, timeout=3)


def _exec(args: list[str], cwd: Path, timeout: int, memory_mb: int | None = None) -> tuple[int, str]:
    limit_mb = memory_mb or memory_limit_mb()
    limit = limit_mb * 1024 * 1024
    # CREATE_NO_WINDOW (no console flashing up) | BELOW_NORMAL_PRIORITY_CLASS
    flags = 0x08000000 | 0x00004000 if WINDOWS else 0
    with _slots:
        proc = subprocess.Popen([_python(), *args], cwd=cwd, env=_env(cwd), stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=flags,
                                start_new_session=not WINDOWS)
        job = _windows_job(proc, limit) if WINDOWS else None
        try:
            ps = psutil.Process(proc.pid)
            if not WINDOWS:
                ps.nice(10)  # lower priority than the app
        except psutil.Error:
            ps = None
        chunks: list[bytes] = []
        flooded = threading.Event()

        def read() -> None:
            kept = seen = 0
            for chunk in iter(lambda: proc.stdout.read1(65536), b""):
                seen += len(chunk)
                if kept < MAX_OUT * 4:  # bytes; a character is at most 4 bytes
                    chunks.append(chunk)
                    kept += len(chunk)
                if seen > MAX_STREAM:
                    flooded.set()
                    return

        reader = threading.Thread(target=read, daemon=True)
        reader.start()
        stopped = ""
        start = time.monotonic()
        while True:
            try:
                proc.wait(POLL)
                break
            except subprocess.TimeoutExpired:
                pass
            if flooded.is_set():
                stopped = (f"\n[stopped: printed more than {MAX_STREAM // 1_000_000} MB of output. "
                           "Is a print inside a loop that never ends?]")
            elif time.monotonic() - start > timeout:
                stopped = f"\n[stopped: exceeded {timeout}s. Infinite loop?]"
            elif ps is not None and _memory(ps) > limit:
                stopped = (f"\n[stopped: used more than {limit_mb} MB of memory. "
                           "Is a list or string growing without end?]")
            if stopped:
                _kill_tree(proc, ps)
                break
        if not stopped and ps is not None:
            _kill_tree(proc, ps)  # anything it started and left running
        code = proc.wait()
        reader.join(3)
        if job:
            k, handle = job
            k.CloseHandle(handle)  # ends anything still in the job
        if proc.stdout:
            proc.stdout.close()
    out = b"".join(chunks).decode("utf-8", "replace")
    if len(out) > MAX_OUT or flooded.is_set():
        out = out[:MAX_OUT] + "\n[output truncated]"
    if stopped:
        out += stopped
        code = 124
    elif code < 0:  # ended by a signal (macOS/Linux), not by this runner
        out += f"\n[stopped: the system ended the program (signal {-code})]"
    elif code != 0 and "MemoryError" in out:
        out += f"\n[stopped: used more than {limit_mb} MB of memory. Is a list or string growing without end?]"
    return code, out


def run_main(files: dict[str, str], main: str, timeout: int = 20, memory_mb: int | None = None) -> dict:
    with tempfile.TemporaryDirectory(prefix="dojo_") as t:
        wd = Path(t)
        _write(wd, files)
        code, out = _exec([main], wd, timeout, memory_mb)
    return {"ok": code == 0, "output": out}


def run_scratch(code: str, timeout: int = 20) -> dict:
    return run_main({"scratch.py": code}, "scratch.py", timeout)


def check(files: dict[str, str], tests: dict[str, str], timeout: int = 20, memory_mb: int | None = None) -> dict:
    with tempfile.TemporaryDirectory(prefix="dojo_") as t:
        wd = Path(t)
        _write(wd, files)
        _write(wd, tests)
        code, out = _exec(["-m", "pytest", "-q", "--tb=short", "-p", "no:cacheprovider",
                           "--disable-warnings", "-W", "ignore"], wd, timeout, memory_mb)
    m = re.search(r"(\d+) passed", out)
    f = re.search(r"(\d+) (failed|error)", out)
    return {"passed": code == 0, "output": out,
            "n_passed": int(m.group(1)) if m else 0, "n_failed": int(f.group(1)) if f else 0}
