"""Dedupe with pluggable survivor strategies."""


def keep_first(group):
    raise NotImplementedError


def keep_last(group):
    raise NotImplementedError


def keep_max(field):
    raise NotImplementedError


def dedupe(rows, key, strategy):
    raise NotImplementedError
