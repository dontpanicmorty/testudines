import logging

log = logging.getLogger(__name__)


def run_step(rows, transform, run_id, max_failures=2):
    results = []
    skipped = 0
    for n, row in enumerate(rows, start=1):
        try:
            results.append(transform(row))
        except ValueError as e:
            skipped += 1
            log.warning("run=%s row=%d skipped: %s", run_id, n, e)
    if skipped > max_failures:
        log.error("run=%s too many failures skipped=%d", run_id, skipped)
        raise RuntimeError(f"run {run_id}: {skipped} rows skipped")
    log.info("run=%s ok=%d skipped=%d", run_id, len(results), skipped)
    return results
