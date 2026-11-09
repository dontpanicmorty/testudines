import json
from pathlib import Path


class TooManyRejects(Exception):
    pass


def load_rows(rows, parse, reject_path, max_reject_rate=0.2):
    # TODO
    pass
