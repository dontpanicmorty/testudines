import httpx
import pytest

from solution import fetch_users_page


def make_client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")


def test_returns_results_and_sends_page():
    seen = []

    def handler(request):
        seen.append((request.url.path, request.url.params.get("page")))
        return httpx.Response(200, json={"page": 2, "results": [{"id": 6, "name": "Ada"}], "next": 3})

    assert fetch_users_page(make_client(handler), 2) == [{"id": 6, "name": "Ada"}]
    assert seen == [("/users", "2")], f"unexpected request: {seen}"


def test_empty_page():
    client = make_client(lambda r: httpx.Response(200, json={"page": 9, "results": [], "next": None}))
    assert fetch_users_page(client, 9) == []


@pytest.mark.parametrize("status", [404, 500, 503])
def test_bad_status_raises(status):
    client = make_client(lambda r: httpx.Response(status, json={"error": "nope"}))
    with pytest.raises(httpx.HTTPStatusError):
        fetch_users_page(client, 1)
