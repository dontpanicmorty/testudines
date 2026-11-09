import urllib.error
import urllib.request


def fetch_or_none(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError:
        return None
