from itertools import islice


def batches(iterable, size):
    if size < 1:
        raise ValueError("size must be >= 1")
    it = iter(iterable)
    while chunk := list(islice(it, size)):
        yield chunk
