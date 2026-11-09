import re


def headings(html):
    found = re.findall(r"<h[12]>(.*?)</h[12]>", html)
    return [text.strip() for text in found]
