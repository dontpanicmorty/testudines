import json


def format_event(event, **fields):
    return json.dumps({"event": event, **fields}, sort_keys=True)


def parse_events(text):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out
