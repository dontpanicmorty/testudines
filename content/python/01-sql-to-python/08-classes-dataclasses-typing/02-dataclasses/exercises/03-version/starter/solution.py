"""Versions."""
from dataclasses import dataclass


@dataclass
class Version:
    major: int
    minor: int = 0
    patch: int = 0
