import pytest
from pydantic import BaseModel
from solution import load_events, TooManyRejects


class Event(BaseModel):
    event_id: str
    user_id: int


GOOD = '{"event_id": "a", "user_id": 1}'


def test_mixed_lines():
    lines = [GOOD, "", '{"event_id": "b", "user_', "[1, 2]", '{"event_id": "c", "user_id": "zz"}',
             '{"event_id": "d", "user_id": 4}', "   ", '{"event_id": "e", "user_id": 5}',
             '{"event_id": "f", "user_id": 6}', '{"event_id": "g", "user_id": 7}']
    valid, rejects = load_events(lines, Event, max_reject_rate=0.5)
    assert [e.event_id for e in valid] == ["a", "d", "e", "f", "g"]
    assert [r["line_no"] for r in rejects] == [3, 4, 5]
    assert rejects[0]["reason"].startswith("invalid json")
    assert rejects[1]["reason"] == "not an object"
    assert rejects[2]["reason"] == "invalid fields: user_id"
    assert rejects[0]["line"] == lines[2]


def test_multiple_fields_sorted():
    valid, rejects = load_events([GOOD] * 9 + ['{"x": 1}'], Event)
    assert rejects[0]["reason"] == "invalid fields: event_id, user_id"


def test_breaker_trips_only_when_strictly_greater():
    lines = [GOOD] * 3 + ["nope"]          # 1/4 = 0.25 -> allowed at 0.25
    valid, rejects = load_events(lines, Event, max_reject_rate=0.25)
    assert len(valid) == 3 and len(rejects) == 1
    with pytest.raises(TooManyRejects):
        load_events([GOOD, "nope"], Event, max_reject_rate=0.25)


def test_empty():
    assert load_events(["", "  "], Event) == ([], [])
    assert load_events([], Event) == ([], [])


def test_accepts_generator():
    assert len(load_events((l for l in [GOOD]), Event)[0]) == 1
