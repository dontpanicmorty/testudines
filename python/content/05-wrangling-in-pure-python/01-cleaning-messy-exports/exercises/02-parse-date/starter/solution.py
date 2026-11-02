from datetime import date, datetime


def parse_date(text):
    # TODO
    return datetime.strptime(text, "%Y-%m-%d").date()
