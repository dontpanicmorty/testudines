from concurrent.futures import ProcessPoolExecutor


def _sum_squares(chunk: list[int]) -> int:
    return sum(n * n for n in chunk)


def sum_of_squares(numbers: list[int], workers: int = 2) -> int:
    if workers < 1:
        raise ValueError("workers must be >= 1")
    if not numbers:
        return 0
    chunks = [numbers[i::workers] for i in range(workers)]
    chunks = [c for c in chunks if c]
    with ProcessPoolExecutor(max_workers=len(chunks)) as pool:
        return sum(pool.map(_sum_squares, chunks))
