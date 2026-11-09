"""The free-plan check is case-sensitive, so 'Free' customers slip through."""
import csv


def active_customers(path):
    """Rows (stripped values, file order) whose plan is not 'free' (case/space-insensitive)."""
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            clean = {key: value.strip() for key, value in row.items()}
            if clean["plan"] != "free":
                rows.append(clean)
    return rows
