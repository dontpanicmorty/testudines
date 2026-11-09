import re
import urllib.request


def outside_links(url):
    with urllib.request.urlopen(url) as response:
        html = response.read().decode("utf-8")
    found = re.findall(r'href="(https?://[^"]*)"', html)
    return sorted(set(found))
