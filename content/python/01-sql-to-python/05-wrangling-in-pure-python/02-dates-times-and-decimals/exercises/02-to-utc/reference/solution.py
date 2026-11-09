from datetime import datetime, timezone


def to_utc(text):
    dt = datetime.fromisoformat(text.strip())
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def event_day(text):
    return to_utc(text).date()
