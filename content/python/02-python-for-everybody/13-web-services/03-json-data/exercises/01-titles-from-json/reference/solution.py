import json


def book_titles(json_text):
    data = json.loads(json_text)
    return [b["title"] for b in data["books"]]
