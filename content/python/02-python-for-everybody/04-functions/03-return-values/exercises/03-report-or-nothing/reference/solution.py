def triangle_perimeter(a, b, c):
    longest = max(a, b, c)
    others = a + b + c - longest
    if others > longest:
        return a + b + c
    return None
