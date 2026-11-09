"""Column descriptions."""
from dataclasses import dataclass, field


@dataclass
class ColumnSpec:
    name: str
    dtype: str
    nullable: bool = True
    tags: list[str] = []


def describe(col):
    suffix = "" if col.nullable else " (not null)"
    return f"{col.name}: {col.dtype}{suffix}"
