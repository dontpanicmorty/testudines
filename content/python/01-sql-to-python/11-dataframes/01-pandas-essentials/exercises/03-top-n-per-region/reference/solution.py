import pandas as pd


def top_n_per_region(df: pd.DataFrame, n: int) -> pd.DataFrame:
    ranked = df.sort_values(["region", "amount"], ascending=[True, False])
    return ranked.groupby("region").head(n).reset_index(drop=True)
