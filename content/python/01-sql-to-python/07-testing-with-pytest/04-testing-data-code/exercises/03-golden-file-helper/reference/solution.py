"""Golden-file assertions."""
import difflib
from pathlib import Path


def assert_matches_golden(actual, golden_path, *, update=False):
    path = Path(golden_path)
    if update:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual)
        return None
    if not path.exists():
        raise AssertionError(f"golden file {path} is missing; create it with update=True")
    expected = path.read_text()
    if expected == actual:
        return None
    diff = "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="golden",
            tofile="actual",
        )
    )
    raise AssertionError(f"output differs from {path.name}:\n{diff}")
