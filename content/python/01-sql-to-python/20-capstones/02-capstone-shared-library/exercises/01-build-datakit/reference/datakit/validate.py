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
        self._required = tuple(required)
        self._types = dict(types or {})
        self._checks = dict(checks or {})

    @staticmethod
    def _missing(value: Any) -> bool:
        return value is None or (isinstance(value, str) and value.strip() == "")

    def errors(self, row: Mapping[str, Any]) -> list[str]:
        problems: list[str] = []
        for name in self._required:
            if self._missing(row.get(name)):
                problems.append(f"{name}: required")
        for name, tp in self._types.items():
            value = row.get(name)
            if self._missing(value):
                continue
            if not isinstance(value, tp) or (tp is not bool and isinstance(value, bool)):
                problems.append(f"{name}: expected {tp.__name__}")
        for name, check in self._checks.items():
            value = row.get(name)
            if self._missing(value):
                continue
            tp = self._types.get(name)
            if tp is not None and (not isinstance(value, tp) or (tp is not bool and isinstance(value, bool))):
                continue
            try:
                ok = bool(check(value))
            except Exception:
                ok = False
            if not ok:
                problems.append(f"{name}: failed check")
        return problems

    def split(self, rows: Iterable[Mapping[str, Any]]) -> tuple[list[dict], list[tuple[dict, list[str]]]]:
        valid: list[dict] = []
        invalid: list[tuple[dict, list[str]]] = []
        for row in rows:
            problems = self.errors(row)
            if problems:
                invalid.append((dict(row), problems))
            else:
                valid.append(dict(row))
        return valid, invalid
