"""Location of everything. Resolved at runtime, never hardcoded to a machine."""
from __future__ import annotations

import os
import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = PACKAGE_DIR / "assets"
# Project root = folder containing pyproject.toml (src/pydojo/../..). Only meaningful in a source checkout.
PROJECT_DIR = PACKAGE_DIR.parent.parent
PACKAGED = os.environ.get("PYDOJO_PACKAGED") == "1"


def _user_data_dir() -> Path:
    """Standard per-user data folder, so an installed app can be replaced without losing progress."""
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "PyDojo"
    if sys.platform == "win32":
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "PyDojo"
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "pydojo"


CONTENT_DIR = Path(os.environ.get("PYDOJO_CONTENT", PROJECT_DIR / "content"))
DATASETS_DIR = Path(os.environ.get("PYDOJO_DATASETS", PROJECT_DIR / "datasets"))
HOME_DIR = Path(os.environ.get("PYDOJO_HOME") or (_user_data_dir() if PACKAGED else PROJECT_DIR / "user_data"))
