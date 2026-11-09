"""Who's practicing: each user has their own folder holding their progress in both sections.

HOME_DIR/users.json             the list of users, in the order they were added
HOME_DIR/settings.json          app settings that aren't per user (the last user, the last section)
HOME_DIR/users/<folder>/        one user's progress.db and scratch pad
"""
from __future__ import annotations

import json
import re
import shutil

from .db import DB
from .paths import HOME_DIR, PY_DOJO_HOME


def _read(name: str, default):
    try:
        return json.loads((HOME_DIR / name).read_text())
    except (OSError, ValueError):
        return default


def _write(name: str, value) -> None:
    HOME_DIR.mkdir(parents=True, exist_ok=True)
    (HOME_DIR / name).write_text(json.dumps(value, indent=2))


def users() -> list[str]:
    return [u for u in _read("users.json", []) if isinstance(u, str) and u.strip()]


def folder(name: str):
    """A user's folder; the name is kept readable but made safe as a folder name."""
    safe = re.sub(r"[^A-Za-z0-9 _.-]+", "_", name.strip()).strip(" .") or "user"
    return HOME_DIR / "users" / safe


def add(name: str) -> str:
    name = name.strip()
    if not name:
        raise ValueError("Enter a name.")
    existing = users()
    if name not in existing:
        first = not existing
        _write("users.json", existing + [name])
        if first:
            adopt_py_dojo_progress(name)
    return name


def remove(name: str) -> None:
    _write("users.json", [u for u in users() if u != name])
    shutil.rmtree(folder(name), ignore_errors=True)


def settings() -> dict:
    return _read("settings.json", {})


def save_setting(key: str, value) -> None:
    s = settings()
    s[key] = value
    _write("settings.json", s)


def last_user() -> str | None:
    name = settings().get("last_user")
    return name if name in users() else None


def open_db(name: str) -> DB:
    return DB(folder(name) / "progress.db")


def adopt_py_dojo_progress(name: str) -> bool:
    """The first user takes over progress from Py Dojo (the Python section's earlier app), if there is any
    and this user has none yet. Py Dojo's own file is copied, never moved."""
    old = PY_DOJO_HOME / "progress.db"
    new = folder(name) / "progress.db"
    if not old.is_file() or new.exists():
        return False
    new.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(old, new)
    scratch = PY_DOJO_HOME / "scratch.py"
    if scratch.is_file():
        shutil.copy2(scratch, new.parent / "scratch.py")
    return True
