import urllib.request


def download(url, dest):
    with urllib.request.urlopen(url) as response:
        data = response.read()
    with open(dest, "wb") as out:
        out.write(data)
    return len(data)
