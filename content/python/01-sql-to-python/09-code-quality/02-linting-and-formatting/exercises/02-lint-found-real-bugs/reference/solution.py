"""Tagging and filter helpers."""


def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


def make_filters(thresholds):
    def at_least(threshold):
        return lambda row: row["value"] >= threshold

    return [at_least(t) for t in thresholds]
