import asyncio

from fastapi.testclient import TestClient

from solution import create_app


async def fast():
    await asyncio.sleep(0.001)
    return "fresh"


async def slow():
    await asyncio.sleep(0.5)
    return "late"


async def broken():
    raise ValueError("warehouse exploded")


def test_success():
    with TestClient(create_app(fast, [], timeout=1.0)) as c:
        r = c.get("/report")
        assert r.status_code == 200 and r.json() == {"report": "fresh"}


def test_timeout_504():
    with TestClient(create_app(slow, [], timeout=0.02)) as c:
        r = c.get("/report")
        assert r.status_code == 504 and r.json() == {"detail": "upstream timed out"}


def test_upstream_error_502_without_leaking():
    with TestClient(create_app(broken, [], timeout=1.0)) as c:
        r = c.get("/report")
        assert r.status_code == 502 and r.json() == {"detail": "upstream failed"}
        assert "exploded" not in r.text


def test_lifespan_events_order():
    events = []
    app = create_app(fast, events, timeout=1.0)
    assert events == []
    with TestClient(app) as c:
        assert events == ["startup"]
        c.get("/health")
    assert events == ["startup", "shutdown"]


def test_health_does_not_call_fetch():
    calls = []

    async def counting():
        calls.append(1)
        return "x"

    with TestClient(create_app(counting, [], timeout=1.0)) as c:
        assert c.get("/health").json() == {"status": "ok"}
    assert calls == []


def test_timeout_does_not_break_later_requests():
    state = {"n": 0}

    async def sometimes():
        state["n"] += 1
        if state["n"] == 1:
            await asyncio.sleep(0.5)
        return "ok"

    with TestClient(create_app(sometimes, [], timeout=0.02)) as c:
        assert c.get("/report").status_code == 504
        assert c.get("/report").json() == {"report": "ok"}
