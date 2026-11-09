def safe_share(total, people):
    try:
        return total / people
    except ZeroDivisionError:
        return None
