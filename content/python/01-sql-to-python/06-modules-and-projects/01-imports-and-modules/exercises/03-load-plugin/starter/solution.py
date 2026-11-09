"""Plugin loader."""
import importlib
import sys


def load_module_from(directory, name):
    """Import module `name` found in `directory` and return it.

    Leaves sys.path unchanged, never returns a stale cached module,
    and does not leave `name` in sys.modules.
    """
    raise NotImplementedError
