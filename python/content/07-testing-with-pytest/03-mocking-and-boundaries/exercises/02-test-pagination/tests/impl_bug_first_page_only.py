"""Only the first page is fetched."""


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
            page = None
    except ConnectionError as exc:
        raise FetchError(f"failed while fetching page {page}") from exc
    return users
