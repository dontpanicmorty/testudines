def swap_ends(text):
    if len(text) < 2:
        return text
    return text[-1] + text[1:-1] + text[0]
