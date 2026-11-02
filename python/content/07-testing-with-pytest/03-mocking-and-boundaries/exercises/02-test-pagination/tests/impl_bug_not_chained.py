"""FetchError is raised without the original ConnectionError as its cause."""


class FetchError(Exception):
    """Raised when the API cannot be read."""


def fetch_all_users(client):
    """Return every user from every page, in order."""
    users = []
    page = 1
    try:
        while page is not None:
            data = client.get_page(page)
            users.extend(data["users"])
            page = data["next_page"]
    except ConnectionError as exc:
        raise FetchError(f"failed while fetching page {page}") from None
    return users
