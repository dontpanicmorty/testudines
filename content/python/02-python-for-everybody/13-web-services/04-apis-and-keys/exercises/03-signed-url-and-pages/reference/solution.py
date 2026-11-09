import json
from urllib.parse import urlencode
from urllib.request import urlopen


def make_request_url(base, params, environ):
    if "PLACE_API_KEY" not in environ:
        raise RuntimeError("PLACE_API_KEY is not set")
    query = dict(params)
    query["key"] = environ["PLACE_API_KEY"]
    return base + "?" + urlencode(query)


def collect_items(first_url):
    items = []
    url = first_url
    while url:
        with urlopen(url, timeout=5) as response:
            page = json.loads(response.read().decode("utf-8"))
        items.extend(page["items"])
        url = page["next"]
    return items
