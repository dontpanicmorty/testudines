def check_contract(func, cases):
    failures = []
    for n, (args, kwargs, expected) in enumerate(cases):
        wants_error = isinstance(expected, type) and issubclass(expected, BaseException)
        try:
            got = func(*args, **kwargs)
        except Exception as exc:
            if wants_error and isinstance(exc, expected):
                continue
            failures.append(f"case {n}: raised {type(exc).__name__}")
            continue
        if wants_error:
            failures.append(f"case {n}: expected {expected.__name__} to be raised")
        elif got != expected:
            failures.append(f"case {n}: expected {expected!r}, got {got!r}")
    return failures
