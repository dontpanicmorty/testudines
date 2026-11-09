def members_by_club(joined):
    clubs = {}
    for name in joined:
        club = joined[name]
        if club not in clubs:
            clubs[club] = []
        clubs[club].append(name)
    for club in clubs:
        clubs[club].sort()
    return clubs
