"""Versions."""
from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Version:
    major: int
    minor: int = 0
    patch: int = 0

    @classmethod
    def parse(cls, text):
        body = text.strip()
        if body[:1] in ("v", "V"):
            body = body[1:]
        parts = body.split(".")
        if not 1 <= len(parts) <= 3 or not all(p.isdigit() for p in parts):
            raise ValueError(f"not a version: {text!r}")
        return cls(*(int(p) for p in parts))

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"
