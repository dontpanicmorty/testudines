import re


def link_targets(html):
    return re.findall(r'href="(.*?)"', html)
