"""Invoice report."""


def parse_rows(csv_text):
    lines = csv_text.strip().splitlines()
    header = lines[0].split(",")
    return [dict(zip(header, line.split(","))) for line in lines[1:] if line.strip()]


def is_paid(row):
    return row["status"].strip().lower() == "paid"


def parse_amount(text):
    return float(text.strip().replace("$", ""))


def totals_by_customer(rows):
    totals = {}
    for row in rows:
        if is_paid(row):
            name = row["customer"].strip()
            totals[name] = totals.get(name, 0) + parse_amount(row["amount"])
    return totals


def format_report(totals):
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    lines = [f"{name}: {total:.2f}" for name, total in ranked]
    lines.append(f"TOTAL: {sum(totals.values()):.2f}")
    return "\n".join(lines)


def process(csv_text):
    return format_report(totals_by_customer(parse_rows(csv_text)))
