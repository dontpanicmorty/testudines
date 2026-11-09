def parse_amounts(values):
    good, rejects = [], []
    for i, v in enumerate(values):
        try:
            text = v.strip() if isinstance(v, str) else v
            good.append(float(text))
        except (ValueError, TypeError):
            rejects.append((i, v))
    return good, rejects
