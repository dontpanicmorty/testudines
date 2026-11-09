"""Header normalisation."""

import re


def clean_header(raw, index):
    """Return a safe column name for one raw header."""
    name = re.sub(r"[^a-z0-9]+", "_", raw.strip().lower()).strip("_")
    return name or f"col_{index}"


def normalize_headers(headers):
    """Normalise headers and make duplicates unique."""
    seen = {}
    result = []
    for index, raw in enumerate(headers):
        name = clean_header(raw, index)
        seen[name] = seen.get(name, 0) + 1
        result.append(name if seen[name] == 1 else f"{name}_{seen[name]}")
    return result
