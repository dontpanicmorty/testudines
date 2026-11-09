def error_name(action):
    try:
        action()
    except Exception as problem:
        return type(problem).__name__
    return "none"
