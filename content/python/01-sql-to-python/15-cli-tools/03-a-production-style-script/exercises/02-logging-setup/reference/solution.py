import logging
import sys


def setup_logging(verbose: bool = False, stream=None) -> logging.Logger:
    log = logging.getLogger("jobrunner")
    for handler in list(log.handlers):
        log.removeHandler(handler)
    handler = logging.StreamHandler(stream if stream is not None else sys.stderr)
    handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    log.addHandler(handler)
    log.setLevel(logging.DEBUG if verbose else logging.INFO)
    log.propagate = False
    return log
