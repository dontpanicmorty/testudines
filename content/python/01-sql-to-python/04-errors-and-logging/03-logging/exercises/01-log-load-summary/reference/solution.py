import logging

log = logging.getLogger(__name__)


def report_load(table, loaded, rejected):
    log.info("loaded table=%s rows=%d", table, loaded)
    if rejected > 0:
        log.warning("rejected table=%s rows=%d", table, rejected)
