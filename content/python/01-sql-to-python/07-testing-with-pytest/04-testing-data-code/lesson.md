+++
id = "testing-with-pytest.testing-data-code"
title = "Testing data code"
minutes = 30
+++

# Testing data code

You already test data with dbt: `unique`, `not_null`, `accepted_values`, and (in newer dbt) unit tests that feed a few mock rows into a model and compare the output. Testing Python transformations follows the same recipe: tiny input, exact expected output, one rule per test.

> **SQL bridge.** A dbt unit test = `given` rows + `expect` rows. A pytest data test = a small list of dicts (or a tiny DataFrame) in, an exact list or frame out. Schema tests (`not_null`, column types) → schema-drift checks.

## Small fixtures beat real extracts

Do not test a transformation against a 2 GB export. Write the **smallest input that exhibits each rule**, three to six rows, with names that tell the story.

```python
def add_order_status(rows):
    out = []
    for r in rows:
        status = "refunded" if r["refund"] > 0 else ("paid" if r["total"] > 0 else "empty")
        out.append({**r, "status": status})
    return out

def test_status_rules():
    given = [
        {"id": 1, "total": 50, "refund": 0},     # normal sale
        {"id": 2, "total": 50, "refund": 20},    # partial refund
        {"id": 3, "total": 0, "refund": 0},      # free sample
    ]
    expected = ["paid", "refunded", "empty"]
    assert [r["status"] for r in add_order_status(given)] == expected

test_status_rules()
print("ok")
```

Note what the test does *not* do: it doesn't compare every column of every row when only `status` is under test. Assert on what the rule is about.

For DataFrames, use the library's own comparison, which gives readable diffs and checks types:

```python
import polars as pl
from polars.testing import assert_frame_equal

def total_by_region(df):
    return df.group_by("region").agg(pl.col("amount").sum().alias("total")).sort("region")

given = pl.DataFrame({"region": ["EU", "US", "EU"], "amount": [10, 5, 7]})
expected = pl.DataFrame({"region": ["EU", "US"], "total": [17, 5]})
assert_frame_equal(total_by_region(given), expected)
print("frames match")
```

Sorting first matters: group-by output order isn't guaranteed, and a test that depends on it is flaky.

## Property: idempotency

A cleaning step is **idempotent** if running it twice gives the same answer as running it once: `f(f(x)) == f(x)`. Pipelines get re-run (retries, backfills), so non-idempotent cleaning corrupts data slowly. Test it directly, over a spread of inputs:

```python
import random

def normalize_name(raw):
    return " ".join(raw.split()).title()

def test_normalize_is_idempotent():
    rng = random.Random(42)                      # seeded: same inputs every run
    alphabet = "abc DEF-'"
    for _ in range(200):
        raw = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
        once = normalize_name(raw)
        assert normalize_name(once) == once, f"not idempotent for {raw!r}"

test_normalize_is_idempotent()
print("idempotent over 200 inputs")
```

Always seed the random generator so a failure can be reproduced. Other useful properties: **row count** never grows after dedupe, **sorted** output stays sorted, **no input mutation**, **totals preserved** across a re-shaping.

## Golden files

For output that is big or fiddly (a rendered report, a generated SQL string), keep the expected output in a file next to the test and compare the whole text. A mismatch shows a diff. When the change is intended, you regenerate the file and review the diff in version control.

```python
import difflib, tempfile
from pathlib import Path

def render(rows):
    return "\n".join(f"{r['region']:<4}{r['total']:>6}" for r in rows) + "\n"

golden = Path(tempfile.mkdtemp()) / "report.golden"
golden.write_text("EU       17\nUS        5\n")

actual = render([{"region": "EU", "total": 17}, {"region": "US", "total": 6}])
expected = golden.read_text()
diff = "".join(difflib.unified_diff(expected.splitlines(True), actual.splitlines(True),
                                    "golden", "actual"))
print(diff or "matches")
```

Golden tests are cheap to write and easy to abuse: if people regenerate them without looking, they stop protecting anything. Keep them for text-shaped output, and review every change.

## Testing for schema drift

Upstream systems rename columns and change types without warning. A **contract test** compares the shape you expect to the shape you got and fails loudly *before* bad data is loaded:

```python
EXPECTED = {"order_id": "int", "placed_at": "str", "total": "float"}

def schema_problems(actual):
    problems = []
    for col in sorted(set(EXPECTED) | set(actual)):
        if col not in actual:
            problems.append(f"missing column: {col}")
        elif col not in EXPECTED:
            problems.append(f"unexpected column: {col}")
        elif EXPECTED[col] != actual[col]:
            problems.append(f"type changed: {col} {EXPECTED[col]} -> {actual[col]}")
    return problems

print(schema_problems({"order_id": "int", "placed_at": "str", "total": "str", "region": "str"}))
```

In real code you read the `actual` schema from the file or table; in the test you feed it known drifted shapes and assert on the messages.

## Common mistakes

- Comparing floats exactly in aggregated output. Use `pytest.approx`, or `assert_frame_equal` with tolerance.
- Depending on row order when the code doesn't promise one: sort before comparing.
- Testing with realistic-looking data that never hits the nasty cases (nulls, duplicates, whitespace, late arrivals). Put those in on purpose.
- Mutating the test input inside the function and then reusing it. Assert the input is unchanged.
- Regenerating golden files blindly.

## What to take away

1. Test transformations with the smallest input that shows each rule, and compare exact outputs.
2. Use `assert_frame_equal` for DataFrames; sort before comparing.
3. Check idempotency: `f(f(x)) == f(x)`, with a seeded random generator.
4. Golden files suit big text outputs; review every regeneration.
5. Add schema-drift checks that fail before bad data lands.
