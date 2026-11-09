"""Helpers for summarising exported order totals."""

ROWS = [10, 20, 30]


def summarize(rows):
    return f"{len(rows)} rows, total {sum(rows)}"


if __name__ == "__main__":
    print(summarize(ROWS))
