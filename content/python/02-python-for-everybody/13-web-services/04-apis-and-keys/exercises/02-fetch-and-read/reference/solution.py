import json
from urllib.request import urlopen


def stations_with_bikes(url, minimum):
    with urlopen(url, timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))
    return [s["name"] for s in data["results"] if s["bikes"] >= minimum]
