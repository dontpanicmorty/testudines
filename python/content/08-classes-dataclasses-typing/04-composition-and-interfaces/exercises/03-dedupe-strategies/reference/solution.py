"""Dedupe with pluggable survivor strategies."""


def keep_first(group):
    return group[0]


def keep_last(group):
    return group[-1]


def keep_max(field):
    def strategy(group):
        return max(group, key=lambda row: row[field])

    return strategy


def dedupe(rows, key, strategy):
    groups = {}
    for row in rows:
        groups.setdefault(row[key], []).append(row)
    return [strategy(group) for group in groups.values()]
