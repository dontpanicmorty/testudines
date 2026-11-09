import urllib.request


def read_page(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")
