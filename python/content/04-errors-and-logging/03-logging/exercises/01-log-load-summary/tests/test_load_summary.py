import logging

from solution import report_load


def test_clean_load(caplog):
    with caplog.at_level(logging.INFO):
        report_load("orders", 10, 0)
    recs = [r for r in caplog.records if r.name == "solution"]
    assert [(r.levelno, r.getMessage()) for r in recs] == [(logging.INFO, "loaded table=orders rows=10")]


def test_with_rejects(caplog):
    with caplog.at_level(logging.INFO):
        report_load("orders", 1204, 12)
    recs = [r for r in caplog.records if r.name == "solution"]
    assert [(r.levelno, r.getMessage()) for r in recs] == [
        (logging.INFO, "loaded table=orders rows=1204"),
        (logging.WARNING, "rejected table=orders rows=12"),
    ]


def test_no_print(capsys):
    report_load("orders", 1, 1)
    assert capsys.readouterr().out == ""
