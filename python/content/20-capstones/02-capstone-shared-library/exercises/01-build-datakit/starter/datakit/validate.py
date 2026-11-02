"""Row validation."""
from typing import Any, Callable, Iterable, Mapping


class RowValidator:
    """Validate dict-like rows against required fields, types and per-field checks."""

    def __init__(
        self,
        *,
        required: Iterable[str] = (),
        types: Mapping[str, type] | None = None,
        checks: Mapping[str, Callable[[Any], bool]] | None = None,
    ) -> None:
        raise NotImplementedError

    def errors(self, row: Mapping[str, Any]) -> list[str]:
        """Return a list of problems, empty when the row is valid."""
        raise NotImplementedError

    def split(self, rows: Iterable[Mapping[str, Any]]) -> tuple[list[dict], list[tuple[dict, list[str]]]]:
        """Return (valid_rows, [(invalid_row, errors), ...]) as copies, in input order."""
        raise NotImplementedError
