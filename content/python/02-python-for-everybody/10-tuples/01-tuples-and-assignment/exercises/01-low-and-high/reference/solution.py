def spread(numbers):
    if len(numbers) == 0:
        return (None, None)
    return (min(numbers), max(numbers))
