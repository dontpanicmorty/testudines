import time


def retry(fn, attempts, is_retryable, base_delay=1.0, sleep=time.sleep):
    for n in range(attempts):
        try:
            return fn()
        except Exception as exc:
            if not is_retryable(exc) or n == attempts - 1:
                raise
            sleep(base_delay * 2 ** n)
