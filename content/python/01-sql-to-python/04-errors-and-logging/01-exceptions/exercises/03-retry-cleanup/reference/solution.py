def load_with_retry(load, attempts, on_close):
    last = None
    try:
        for _ in range(attempts):
            try:
                return load()
            except ConnectionError as e:
                last = e
        raise ConnectionError(f"giving up after {attempts} attempts") from last
    finally:
        on_close()
