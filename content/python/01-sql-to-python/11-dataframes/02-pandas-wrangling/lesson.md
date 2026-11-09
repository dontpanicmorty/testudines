+++
id = "dataframes.pandas-wrangling"
title = "pandas wrangling: cleaning messy data"
minutes = 30
+++

# pandas wrangling: cleaning messy data

Real exports are dirty: padded headers, `$` in numbers, three date formats, `N/A` where a number should be, duplicated rows. In SQL you would chain `TRIM`, `REPLACE`, `TRY_CAST`, `COALESCE` and `QUALIFY ROW_NUMBER()`. In pandas the same cleaning is a pipeline of column operations. We will clean the bundled `messy_invoices.csv` step by step.

> **SQL bridge.** `TRIM/LOWER/REPLACE` → `.str.strip()/.str.lower()/.str.replace()`. `TRY_CAST(x AS FLOAT)` → `pd.to_numeric(x, errors="coerce")`. `COALESCE(x, 0)` → `x.fillna(0)`. `QUALIFY ROW_NUMBER() = 1` → `drop_duplicates()`.

## Look first

```python
import os
import pandas as pd

raw = pd.read_csv(os.path.join(os.environ["DOJO_DATA"], "messy_invoices.csv"))
print(list(raw.columns))
print(raw.head(3))
print(raw.isna().sum())
```

Always look at `columns`, `head()` and the missing counts before writing a single cleaning step. Note the header names have spaces, capitals and a `#`.

## Headers

```python
import re
import pandas as pd

cols = ["Invoice #", "Customer Name ", "AMOUNT"]
clean = [re.sub(r"[^a-z0-9]+", "_", c.strip().lower()).strip("_") for c in cols]
print(clean)
```

Apply it with `df.columns = [...]` or `df.rename(columns=...)`. Normalised, predictable column names are the single cheapest data-quality win.

## Strings, numbers and missing data

The `.str` accessor applies string methods to a whole column and passes missing values through.

```python
import pandas as pd

amount = pd.Series(["1310.11", "$3,291.26", "N/A", "", None, " 99.00 "])
cleaned = amount.str.strip().str.replace(r"[$,]", "", regex=True)
numbers = pd.to_numeric(cleaned, errors="coerce")
print(numbers.tolist())
print(numbers.isna().sum(), "missing")
```

`errors="coerce"` turns anything unparseable (`"N/A"`, `""`) into `NaN` instead of raising, the equivalent of `TRY_CAST`. You decide afterwards what a missing amount means: `fillna(0)`, drop the row, or flag it. Do not decide by accident.

Names and statuses use the same tools:

```python
import pandas as pd

names = pd.Series(["MARGARET LISKOV", "  barbara liskov ", "Ada Turing"])
print(names.str.strip().str.title().tolist())
status = pd.Series(["Paid", "PAID ", "paid", None, "overdue"])
print(status.str.strip().str.lower().fillna("unknown").value_counts().to_dict())
```

## Dates in several formats

```python
import pandas as pd

dates = pd.Series(["2025-09-26", "05/26/2025", "20 Jun 2025", "garbage"])
parsed = pd.to_datetime(dates, format="mixed", errors="coerce")
print(parsed.dt.strftime("%Y-%m-%d").tolist())
```

`format="mixed"` guesses each value on its own. Be aware that `03/04/2025` is ambiguous (March 4th or April 3rd?) and the default reads it month-first. If you know the format, give it: `format="%m/%d/%Y"`. When data has several known formats, parse each with its format and combine, which removes the guessing:

```python
import pandas as pd

dates = pd.Series(["2025-09-26", "05/26/2025", "20 Jun 2025"])
out = pd.Series(pd.NaT, index=dates.index, dtype="datetime64[us]")
for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d %b %Y"]:
    out = out.fillna(pd.to_datetime(dates, format=fmt, errors="coerce"))
print(out.dt.strftime("%Y-%m-%d").tolist())
```

## Duplicates

```python
import pandas as pd

df = pd.DataFrame({"inv": ["A", "A", "B"], "amt": [1.0, 1.0, 2.0], "seen": [1, 2, 3]})
print(df.drop_duplicates())                       # whole-row duplicates
print(df.drop_duplicates(subset="inv", keep="last"))  # latest per key
```

`subset` names the business key, `keep` picks the survivor. Sort first when "latest" depends on a timestamp.

## Reshaping: pivot and melt

```python
import pandas as pd

sales = pd.DataFrame({
    "region": ["east", "east", "west", "west"],
    "quarter": ["Q1", "Q2", "Q1", "Q2"],
    "revenue": [10, 20, 5, 7],
})
wide = sales.pivot_table(index="region", columns="quarter", values="revenue", aggfunc="sum").reset_index()
print(wide)
long = wide.melt(id_vars="region", var_name="quarter", value_name="revenue")
print(long)
```

`pivot_table` is conditional aggregation (`SUM(CASE WHEN quarter='Q1' ...)`); `melt` is `UNPIVOT`.

## Traps

**Writing to a slice.** Selecting rows then assigning into the result modifies a *temporary*, not your frame. Use `.loc[mask, column] = value` on the frame itself:

```python
import pandas as pd

df = pd.DataFrame({"amt": [5, 50, 500]})
df[df["amt"] > 10]["amt"] = 0            # chained: changes a temporary copy
print(df["amt"].tolist())
df.loc[df["amt"] > 10, "amt"] = 0        # correct
print(df["amt"].tolist())
```

In older pandas this was the infamous `SettingWithCopyWarning`. In current pandas you get `ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment` on stderr, and the data is still unchanged. Either way: one `.loc` assignment.

**Integers that become floats.** An int column with a missing value cannot be a plain NumPy int, so it silently becomes `float` (`3` turns into `3.0`). Use the nullable `Int64` dtype when you need integers with gaps:

```python
import pandas as pd

print(pd.Series([1, 2, None]).tolist())
print(pd.Series([1, 2, None], dtype="Int64").tolist())
```

## Common mistakes

- `AttributeError: Can only use .str accessor with string values!` the column is numeric or mixed after an earlier step. Check `df.dtypes`.
- Cleaning in place across many cells and forgetting which version of the frame you are on. Prefer one `assign`/method chain from raw to clean.
- Dropping duplicates before normalising names: `"Ada"` and `"ada "` are different strings until you clean them.
- Using `fillna(0)` on amounts so that missing becomes a real zero in your totals.

## What to take away

1. Inspect first: columns, `head()`, missing counts.
2. `.str` methods and `to_numeric(errors="coerce")` replace `TRIM`, `REPLACE` and `TRY_CAST`.
3. Parse dates with explicit formats when you can; `format="mixed"` guesses.
4. `drop_duplicates(subset=..., keep=...)` is your `QUALIFY ROW_NUMBER() = 1`.
5. Assign with `.loc[mask, col]`, never a chained selection, and use `Int64` for integers with gaps.
