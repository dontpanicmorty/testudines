from urllib.parse import urlencode


def build_url(base, params):
    if not params:
        return base
    return base + "?" + urlencode(params)
