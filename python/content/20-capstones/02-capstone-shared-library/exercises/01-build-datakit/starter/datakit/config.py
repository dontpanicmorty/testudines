"""Typed configuration loader."""
from typing import Mapping, TypeVar

T = TypeVar("T")


def load_config(cls: type[T], source: Mapping[str, str] | None = None, prefix: str = "") -> T:
    """Build ``cls`` (a dataclass) from ``source`` (default: os.environ).

    Field ``max_rows`` is read from ``{prefix}MAX_ROWS``. Report ALL problems together
    in one ConfigError.
    """
    raise NotImplementedError
