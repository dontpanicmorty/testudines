def slugify(text):
    """Turn text into a URL-friendly slug.

    >>> slugify("Daily Orders Report")
    'daily-orders-report'
    >>> slugify("  Extra   spaces ")
    'extra-spaces'
    >>> slugify("Q1: Revenue (EUR)")
    'q1-revenue-eur'
    >>> slugify("---")
    ''
    """
    return text
