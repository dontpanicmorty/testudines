import logging


def make_logger(name, path, level=logging.INFO):
    log = logging.getLogger(name)
    log.setLevel(level)
    log.propagate = False
    if not log.handlers:
        handler = logging.FileHandler(path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
        log.addHandler(handler)
    return log
