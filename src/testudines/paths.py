"""Location of everything. Resolved at runtime, never hardcoded to a machine."""
from __future__ import annotations

import os
import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = PACKAGE_DIR / "assets"
# Project root = folder containing pyproject.toml (src/testudines/../..). Only meaningful in a source checkout.
PROJECT_DIR = PACKAGE_DIR.parent.parent
PACKAGED = os.environ.get("TESTUDINES_PACKAGED") == "1"


def _user_data_dir(name: str = "Testudines") -> Path:
    """Standard per-user data folder, so an installed app can be replaced without losing progress."""
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / name
    if sys.platform == "win32":
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / name
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / name.lower()


CONTENT_DIR = Path(os.environ.get("TESTUDINES_CONTENT", PROJECT_DIR / "content"))
PY_CONTENT_DIR = CONTENT_DIR / "python"
SQL_CONTENT_DIR = CONTENT_DIR / "sql"
DATASETS_DIR = Path(os.environ.get("TESTUDINES_DATASETS", PROJECT_DIR / "datasets"))
HOME_DIR = Path(os.environ.get("TESTUDINES_HOME") or (_user_data_dir() if PACKAGED else PROJECT_DIR / "user_data"))
# Where Py Dojo kept its progress, so the first user can bring it along (see users.adopt_py_dojo_progress)
PY_DOJO_HOME = _user_data_dir("PyDojo")
