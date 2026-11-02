"""Event routing with a structural Sink type."""
from typing import Protocol, TypedDict


class Event(TypedDict):
    user_id: int
    name: str
    value: float


class Sink(Protocol):
    def write(self, events: list[Event]) -> int: ...


class ListSink:
    """Collects events in `self.events`; `write` returns how many it stored."""

    def __init__(self) -> None:
        self.events: list[Event] = []

    def write(self, events: list[Event]) -> int:
        self.events.extend(events)
        return len(events)


def route(events: list[Event], sink: Sink, *, min_value: float = 0.0) -> int:
    """Send events with value >= min_value to the sink in one call."""
    selected = [e for e in events if e["value"] >= min_value]
    if not selected:
        return 0
    return sink.write(selected)
