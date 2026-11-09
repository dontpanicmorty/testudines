import os
import tempfile
from pathlib import Path


def atomic_write(path, produce):
    # TODO: temp file in the same directory, then os.replace; clean up on error
    pass
