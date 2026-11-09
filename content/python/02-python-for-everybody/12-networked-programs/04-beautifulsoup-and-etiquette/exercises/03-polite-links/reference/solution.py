import urllib.error
import urllib.request

from bs4 import BeautifulSoup


def allowed_links(base_url):
    blocked = []
    try:
        with urllib.request.urlopen(base_url + "/robots.txt") as response:
            rules = response.read().decode("utf-8")
        for line in rules.splitlines():
            name, _, value = line.partition(":")
            if name.strip().lower() == "disallow" and value.strip() != "":
                blocked.append(value.strip())
    except urllib.error.HTTPError:
        pass
    with urllib.request.urlopen(base_url + "/") as response:
        html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for tag in soup.find_all("a"):
        href = tag.get("href")
        if href is None:
            continue
        if any(href.startswith(prefix) for prefix in blocked):
            continue
        links.append(href)
    return links
