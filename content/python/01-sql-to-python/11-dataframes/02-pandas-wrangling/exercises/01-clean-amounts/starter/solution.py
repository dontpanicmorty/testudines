import pandas as pd


def clean_amounts(s: pd.Series) -> pd.Series:
    """Messy money strings -> float Series with NaN for bad values."""
    raise NotImplementedError
