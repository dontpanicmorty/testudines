import inspect

import httpx
import pytest

from solution import iter_events

PAGES = {
    None: {"data": [{"id": 1}, {"id": 2}], "next_cursor": "c2"},
    "c2": {"data": [{"id": 3}], "next_cursor": "c3"},
    "c3": {"data": [], "next_cursor": "c4"},
    "c4": {"data": [{"id": 4}], "next_cursor": None},
}


def make(log, pages=PAGES, status=200):
    def handler(request):
        cur = request.url.params.get("cursor")
        log.append(cur)
        return httpx.Response(status, json=pages.get(cur, {}))

    return httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")


def test_all_events_in_order():
    log = []
    assert [e["id"] for e in iter_events(make(log))] == [1, 2, 3, 4]
    assert log == [None, "c2", "c3", "c4"]


def test_is_a_generator_and_lazy():
    log = []
    gen = iter_events(make(log))
    assert inspect.isgenerator(gen), "iter_events should be a generator (use yield)"
    assert log == [], "no request should happen before iteration starts"
    assert next(gen) == {"id": 1}
    assert log == [None], f"only the first page should be fetched, got {log}"


def test_first_request_has_no_cursor_param():
    seen = []

    def handler(request):
        seen.append("cursor" in request.url.params)
        return httpx.Response(200, json={"data": [], "next_cursor": None})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")
    assert list(iter_events(client)) == []
    assert seen == [False]


def test_bad_status_raises():
    with pytest.raises(httpx.HTTPStatusError):
        list(iter_events(make([], status=500)))
