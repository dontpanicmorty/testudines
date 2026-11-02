def load_with_retry(load, attempts, on_close):
    for _ in range(attempts):
        try:
            result = load()
            on_close()
            return result
        except Exception:
            pass
