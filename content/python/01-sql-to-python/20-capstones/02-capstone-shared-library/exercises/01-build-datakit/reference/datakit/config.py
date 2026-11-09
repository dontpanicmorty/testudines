"""Typed configuration loader."""
import dataclasses
import os
import types
import typing
from typing import Mapping, TypeVar

from .errors import ConfigError

T = TypeVar("T")
_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off"}


def _unwrap_optional(tp):
    if typing.get_origin(tp) in (typing.Union, types.UnionType):
        args = [a for a in typing.get_args(tp) if a is not type(None)]
        if len(args) == 1 and len(typing.get_args(tp)) == 2:
            return args[0], True
    return tp, False


def _parse(raw: str, tp: type):
    text = raw.strip()
    if tp is bool:
        low = text.lower()
        if low in _TRUE:
            return True
        if low in _FALSE:
            return False
        raise ValueError("a boolean")
    if tp is int:
        return int(text)
    if tp is float:
        return float(text)
    return raw


def load_config(cls: type[T], source: Mapping[str, str] | None = None, prefix: str = "") -> T:
    """Build ``cls`` (a dataclass) from ``source`` (default: os.environ).

    Field ``max_rows`` is read from ``{prefix}MAX_ROWS``. All problems are reported together.
    """
    if not dataclasses.is_dataclass(cls) or not isinstance(cls, type):
        raise TypeError("load_config needs a dataclass type")
    env = os.environ if source is None else source
    hints = typing.get_type_hints(cls)
    values: dict = {}
    errors: list[str] = []
    for f in dataclasses.fields(cls):
        if not f.init:
            continue
        key = f"{prefix}{f.name.upper()}"
        tp, optional = _unwrap_optional(hints[f.name])
        if key not in env:
            has_default = f.default is not dataclasses.MISSING or f.default_factory is not dataclasses.MISSING
            if has_default:
                continue
            if optional:
                values[f.name] = None
                continue
            errors.append(f"{key}: missing")
            continue
        try:
            values[f.name] = _parse(env[key], tp)
        except ValueError:
            errors.append(f"{key}: cannot parse {env[key]!r} as {tp.__name__}")
    if errors:
        raise ConfigError(errors)
    return cls(**values)
