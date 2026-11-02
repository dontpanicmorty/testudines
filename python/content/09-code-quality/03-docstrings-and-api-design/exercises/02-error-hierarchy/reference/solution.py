"""A small CSV loader with its own error types."""


class LoadError(Exception):
    """Base class for all errors raised by this loader."""


class SchemaError(LoadError):
    """The header is missing required columns."""

    def __init__(self, missing):
        self.missing = sorted(missing)
        super().__init__("missing columns: " + ", ".join(self.missing))


class RowError(LoadError):
    """A data row is malformed."""

    def __init__(self, line_number, message):
        self.line_number = line_number
        super().__init__(f"line {line_number}: {message}")


def load_rows(lines, required=("id", "amount")):
    iterator = iter(lines)
    header_line = next(iterator, None)
    header = [c.strip() for c in header_line.split(",")] if header_line is not None else []
    missing = [c for c in required if c not in header]
    if missing:
        raise SchemaError(missing)
    rows = []
    for number, line in enumerate(iterator, start=2):
        if not line.strip():
            continue
        cells = [c.strip() for c in line.split(",")]
        if len(cells) != len(header):
            raise RowError(number, f"expected {len(header)} fields, got {len(cells)}")
        rows.append(dict(zip(header, cells, strict=True)))
    return rows
