"""Golden-file assertions."""
import difflib
from pathlib import Path


def assert_matches_golden(actual, golden_path, *, update=False):
    raise NotImplementedError
