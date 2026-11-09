"""Tagging and filter helpers."""


def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags


def make_filters(thresholds):
    filters = []
    for t in thresholds:
        filters.append(lambda row: row["value"] >= t)
    return filters
