def raw_calories(steps, weight_kg):
    return steps * weight_kg * 0.0005


def tidy(number):
    return round(number, 1)


def walk_calories(steps, weight_kg):
    return tidy(raw_calories(steps, weight_kg))
