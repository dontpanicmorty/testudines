"""Event routing with a structural Sink type."""
from typing import Protocol, TypedDict


class Event(TypedDict):
    # TODO: user_id (int), name (str), value (float)
    pass


class Sink(Protocol):
    def write(self, events: list[Event]) -> int: ...


class ListSink:
    """Collects events in `self.events`; `write` returns how many it stored."""


def route(events, sink, *, min_value=0.0):
    """Send events with value >= min_value to the sink in one call."""
    raise NotImplementedError
