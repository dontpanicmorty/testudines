import pandas as pd


def clean_amounts(s: pd.Series) -> pd.Series:
    """Messy money strings -> float Series with NaN for bad values."""
    text = s.astype("string").str.strip().str.replace(r"[$,]", "", regex=True)
    return pd.to_numeric(text, errors="coerce").astype("float64")
