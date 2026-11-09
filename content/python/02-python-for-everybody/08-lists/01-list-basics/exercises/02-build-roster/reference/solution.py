def register(roster, newcomers):
    for name in newcomers:
        if name not in roster:
            roster.append(name)
    roster.sort()
    return roster
