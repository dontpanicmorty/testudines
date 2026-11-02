import sys
import os
import json
from typing import List, Dict


def read_config(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except:
        return None
    count = len(data)
    return data


def has_key(config, key):
    if config == None:
        return False
    if config.get(key) == None:
        return False
    return True


names: List[str] = []
add_name = lambda n: names.append(n)
