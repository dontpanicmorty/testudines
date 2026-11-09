import inspect

POK = inspect.Parameter.POSITIONAL_OR_KEYWORD
KW = inspect.Parameter.KEYWORD_ONLY


def is_breaking(old, new):
    o = inspect.signature(old).parameters
    n = inspect.signature(new).parameters
    for name, p in o.items():
        if name not in n:
            return True
        q = n[name]
        if p.kind is POK and q.kind is KW:
            return True
        if p.default is not p.empty and q.default is q.empty:
            return True
    for name, q in n.items():
        if name not in o and q.default is q.empty:
            return True
    old_pos = [name for name, p in o.items() if p.kind is POK]
    new_pos = [name for name, p in n.items() if p.kind is POK]
    return new_pos[: len(old_pos)] != old_pos
