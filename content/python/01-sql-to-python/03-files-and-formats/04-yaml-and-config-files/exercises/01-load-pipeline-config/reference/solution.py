import yaml


def load_config(path):
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    if "name" not in raw:
        raise KeyError("name")
    cfg = {"retries": 3, "sources": []}
    cfg.update(raw)
    return cfg
