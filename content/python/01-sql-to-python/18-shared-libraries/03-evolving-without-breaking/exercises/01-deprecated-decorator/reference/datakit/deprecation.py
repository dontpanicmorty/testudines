import functools
import warnings


def deprecated(use_instead, removed_in=None):
    def decorator(fn):
        message = f"{fn.__name__} is deprecated, use {use_instead}"
        if removed_in:
            message += f" (removed in {removed_in})"

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
