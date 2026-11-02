import httpx
import pytest

from solution import ApiError, get_json


def make_client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")


def test_success_returns_json():
    client = make_client(lambda r: httpx.Response(200, json={"id": 1}))
    assert get_json(client, "/users/1") == {"id": 1}


@pytest.mark.parametrize("status", [400, 404, 429, 500, 503])
def test_error_status_raises_with_code(status):
    client = make_client(lambda r: httpx.Response(status, json={"error": "x"}))
    with pytest.raises(ApiError) as info:
        get_json(client, "/x")
    assert info.value.status_code == status


def test_timeout_becomes_api_error_without_status():
    def handler(request):
        raise httpx.ReadTimeout("slow", request=request)

    with pytest.raises(ApiError) as info:
        get_json(make_client(handler), "/slow")
    assert info.value.status_code is None


def test_201_counts_as_success():
    client = make_client(lambda r: httpx.Response(201, json={"ok": True}))
    assert get_json(client, "/x") == {"ok": True}
