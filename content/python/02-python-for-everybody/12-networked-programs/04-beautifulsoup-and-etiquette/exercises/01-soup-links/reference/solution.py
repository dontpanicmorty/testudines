from bs4 import BeautifulSoup


def hrefs_in(html):
    soup = BeautifulSoup(html, "html.parser")
    found = []
    for tag in soup.find_all("a"):
        href = tag.get("href")
        if href is not None:
            found.append(href)
    return found
