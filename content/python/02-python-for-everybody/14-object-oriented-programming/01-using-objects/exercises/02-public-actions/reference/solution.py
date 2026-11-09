def actions(obj):
    return sorted(n for n in dir(obj) if not n.startswith("_") and callable(getattr(obj, n)))
