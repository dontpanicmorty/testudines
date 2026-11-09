import pandas as pd

FORMATS = ["%Y-%m-%d", "%m/%d/%Y", "%d %b %Y"]


def parse_dates(s: pd.Series) -> pd.Series:
    """Parse the three known date formats; NaT otherwise."""
    text = s.astype("string").str.strip()
    out = pd.to_datetime(text, format=FORMATS[0], errors="coerce")
    for fmt in FORMATS[1:]:
        out = out.fillna(pd.to_datetime(text, format=fmt, errors="coerce"))
    return out
