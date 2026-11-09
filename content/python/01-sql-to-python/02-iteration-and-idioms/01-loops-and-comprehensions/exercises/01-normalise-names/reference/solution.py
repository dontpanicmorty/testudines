def normalise_names(names):
    return [n.strip().title() for n in names if n is not None and n.strip()]
