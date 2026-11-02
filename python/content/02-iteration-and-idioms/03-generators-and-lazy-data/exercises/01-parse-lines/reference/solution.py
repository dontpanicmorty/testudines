def parse_lines(lines):
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        order_id, amount = line.split(",", 1)
        yield order_id.strip(), float(amount)
