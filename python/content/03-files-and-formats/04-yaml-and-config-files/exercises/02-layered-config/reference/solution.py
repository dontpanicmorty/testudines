import copy


def _deep_merge(base, override):
    out = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def _convert(text, current):
    if isinstance(current, bool):
        return text.strip().lower() in {"1", "true", "yes"}
    if isinstance(current, int):
        return int(text)
    return text


def build_config(defaults, file_cfg, env, prefix="APP_"):
    cfg = _deep_merge(defaults, file_cfg or {})
    for key in list(cfg):
        name = prefix + key.upper()
        if name in env:
            cfg[key] = _convert(env[name], cfg[key])
    return cfg
