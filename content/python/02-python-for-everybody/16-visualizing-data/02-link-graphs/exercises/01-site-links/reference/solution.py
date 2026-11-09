import re


def internal_links(html, known):
    hrefs = re.findall(r'href="([^"]+)"', html)
    return sorted({h for h in hrefs if h in known})
