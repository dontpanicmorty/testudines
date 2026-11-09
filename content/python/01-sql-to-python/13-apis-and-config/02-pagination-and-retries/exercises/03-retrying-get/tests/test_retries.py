import httpx
import pytest

from solution import RetryExhausted, get_with_retries


def scripted(steps):
    """steps: ints (status), ('429', retry_after) tuples or exceptions."""
    it = iter(steps)
    calls = []

    def handler(request):
        calls.append(request.url.path)
        step = next(it)
        if isinstance(step, Exception):
            raise step
        if isinstance(step, tuple):
            return httpx.Response(step[0], headers={"Retry-After": str(step[1])}, json={})
        return httpx.Response(step, json={"ok": step == 200})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")
    return client, calls


def test_success_first_try_no_sleep():
    client, calls = scripted([200])
    slept = []
    assert get_with_retries(client, "/r", sleep=slept.append) == {"ok": True}
    assert slept == [] and len(calls) == 1


def test_5xx_then_success_uses_exponential_waits():
    client, calls = scripted([503, 500, 200])
    slept = []
    assert get_with_retries(client, "/r", sleep=slept.append) == {"ok": True}
    assert slept == [0.5, 1.0]
    assert len(calls) == 3


def test_429_honours_retry_after():
    client, _ = scripted([503, (429, 3), 200])
    slept = []
    get_with_retries(client, "/r", sleep=slept.append)
    assert slept == [0.5, 3.0]


def test_timeout_is_retried():
    def boom():
        return httpx.ReadTimeout("slow")

    client, calls = scripted([boom(), 200])
    slept = []
    assert get_with_retries(client, "/r", sleep=slept.append) == {"ok": True}
    assert slept == [0.5]


@pytest.mark.parametrize("status", [400, 401, 404, 422])
def test_client_errors_not_retried(status):
    client, calls = scripted([status, 200])
    slept = []
    with pytest.raises(httpx.HTTPStatusError):
        get_with_retries(client, "/r", sleep=slept.append)
    assert len(calls) == 1, "4xx must not be retried"
    assert slept == []


def test_exhaustion_raises_without_trailing_sleep():
    client, calls = scripted([500, 500, 500])
    slept = []
    with pytest.raises(RetryExhausted):
        get_with_retries(client, "/r", max_attempts=3, sleep=slept.append)
    assert len(calls) == 3
    assert slept == [0.5, 1.0], f"should not sleep after the last attempt: {slept}"
