"""mylib: small helpers for tidying exported data."""
from .cleaning import clean_name
from .rows import read_rows

__all__ = ["clean_name", "read_rows"]
__version__ = "0.1.0"
