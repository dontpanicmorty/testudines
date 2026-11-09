import pytest

from users_api import FetchError, fetch_all_users


class FakeClient:
    def __init__(self, pages):
        self.pages = pages
        self.calls = []

    def get_page(self, n):
        self.calls.append(n)
        return self.pages[n]


class DownClient:
    def get_page(self, n):
        raise ConnectionError("down")


@pytest.fixture
def client():
    return FakeClient(
        {
            1: {"users": [{"id": 1}, {"id": 2}], "next_page": 2},
            2: {"users": [{"id": 3}], "next_page": 3},
            3: {"users": [{"id": 4}, {"id": 5}], "next_page": None},
        }
    )


def test_collects_all_pages_in_order(client):
    assert fetch_all_users(client) == [{"id": i} for i in (1, 2, 3, 4, 5)]


def test_requests_pages_one_to_three_once(client):
    fetch_all_users(client)
    assert client.calls == [1, 2, 3]


def test_single_page():
    one = FakeClient({1: {"users": [{"id": 9}], "next_page": None}})
    assert fetch_all_users(one) == [{"id": 9}]


def test_connection_error_becomes_fetch_error():
    with pytest.raises(FetchError) as info:
        fetch_all_users(DownClient())
    assert isinstance(info.value.__cause__, ConnectionError)
