"""Plugin loader."""
import importlib
import sys


def load_module_from(directory, name):
    """Import module `name` found in `directory` and return it.

    Leaves sys.path unchanged, never returns a stale cached module,
    and does not leave `name` in sys.modules.
    """
    directory = str(directory)
    sys.modules.pop(name, None)
    importlib.invalidate_caches()
    sys.path.insert(0, directory)
    try:
        return importlib.import_module(name)
    finally:
        sys.path.remove(directory)
        sys.modules.pop(name, None)
