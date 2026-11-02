import logging
import sys


def setup_logging(verbose: bool = False, stream=None) -> logging.Logger:
    log = logging.getLogger("jobrunner")
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler(stream or sys.stderr))
    return log
