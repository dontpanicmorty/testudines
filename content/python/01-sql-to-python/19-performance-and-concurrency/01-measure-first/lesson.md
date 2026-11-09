+++
id = "performance-and-concurrency.measure-first"
title = "Measure first"
minutes = 30
+++

# Measure first

Slow code is rarely slow where you think it is. Every analytics engineer has "optimised" a CTE only to find the real cost was a fan-out join three steps earlier. Python is the same: guess, and you will spend a day speeding up the 2% that never mattered.

> **SQL bridge.** You never tune a query without `EXPLAIN` or the query profile. The Python equivalents are `time.perf_counter` (stopwatch), `timeit` (careful micro-benchmark) and `cProfile` (the query profile: which function ate the time).

The rule for this lesson: **measure, find the one hot spot, fix that, measure again.**

## A stopwatch you can trust

Use `time.perf_counter()`. It is a monotonic high-resolution clock meant for measuring durations. (`time.time()` can jump when the system clock is adjusted.)

```python
import time

start = time.perf_counter()
total = sum(i * i for i in range(1_000_000))
elapsed = time.perf_counter() - start
print(total, elapsed > 0)
```

One run is noisy: the machine was busy, a cache was cold. For small snippets, let `timeit` repeat it and take the **minimum**, because noise only ever makes things slower.

```python
import timeit

runs = timeit.repeat("sum(range(1000))", number=2000, repeat=5)
best_per_call = min(runs) / 2000
print(best_per_call > 0)
```

`number` is how many calls per run; `repeat` is how many runs. Report `min(runs) / number`.

## Big-O intuition with real sizes

Big-O sounds academic until you see how it bites. Looking up "is this id one of my 20,000 ids?":

- in a **list** Python compares item by item: cost grows with the list (`O(n)`)
- in a **set** or **dict** it hashes the value and jumps straight there (`O(1)` on average)

```python
import timeit

ids = list(range(20_000))
ids_set = set(ids)
target = 19_999            # worst case for the list

t_list = min(timeit.repeat(lambda: target in ids, number=200, repeat=3))
t_set = min(timeit.repeat(lambda: target in ids_set, number=200, repeat=3))
print("set is at least 100x faster:", t_list / t_set > 100)
```

Now multiply: if you do that lookup once per row of a 20,000-row table, the list version does 20,000 x 10,000 = **200 million** comparisons. The set version does 20,000.

| Structure | `x in s` | Good for |
|---|---|---|
| `list` | scans, `O(n)` | order matters, small sizes |
| `set` | hash, `O(1)` | membership, dedupe |
| `dict` | hash, `O(1)` | lookup by key (your join index) |

## The accidental quadratic join

This is the single most common performance bug in data code. You have orders and customers, and you "join" them with a loop inside a loop:

```python
def add_region_slow(orders, customers):
    out = []
    for o in orders:
        for c in customers:                 # scans ALL customers for EVERY order
            if c["customer_id"] == o["customer_id"]:
                out.append({**o, "region": c["region"]})
                break
    return out

# The fix is what a database does: build a hash index once, then probe it.
def add_region_fast(orders, customers):
    region_by_id = {c["customer_id"]: c["region"] for c in customers}   # build once
    return [{**o, "region": region_by_id[o["customer_id"]]}
            for o in orders if o["customer_id"] in region_by_id]        # probe per order

customers = [{"customer_id": i, "region": "west" if i % 2 else "east"} for i in range(2000)]
orders = [{"order_id": n, "customer_id": n % 2000} for n in range(2000)]

import time
t = time.perf_counter(); slow = add_region_slow(orders, customers); t_slow = time.perf_counter() - t
t = time.perf_counter(); fast = add_region_fast(orders, customers); t_fast = time.perf_counter() - t
print(slow == fast, t_slow > t_fast)
```

The fix is exactly what a database does: **build a hash index once, then probe it** (the `region_by_id` dict above). Both versions are in the example so you can compare them.

> **Predict first.** If you double both tables, roughly how much longer does the slow version take? Four times: `n x n`. The fast version takes about twice as long: `n + n`.

Same result, very different growth. At 2,000 rows you will not notice. At 2,000,000 the slow version never finishes.

## Reading a profile

When you do not know *where* the time goes, profile. `cProfile` records how many times each function was called and how long it took.

```python
import cProfile
import pstats

def parse(line):
    return [int(x) for x in line.split(",")]

def load(n):
    lines = ["1,2,3"] * n
    return [parse(line) for line in lines]

profiler = cProfile.Profile()
profiler.enable()
load(5000)
profiler.disable()

stats = pstats.Stats(profiler)
calls = {func[2]: info[0] for func, info in stats.stats.items()}
print("parse called", calls["parse"], "times")
```

To see the full table interactively you would write `stats.sort_stats("cumulative").print_stats(10)`, which prints something like:

```text
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.001    0.001    0.012    0.012 demo.py:7(load)
     5000    0.004    0.000    0.010    0.000 demo.py:4(parse)
```

- **ncalls**: how many times it ran. A huge number is your first clue (the quadratic loop body).
- **tottime**: time inside the function itself, *excluding* functions it called.
- **cumtime**: time including everything it called. Sort by this to find the expensive branch of the call tree, then by `tottime` to find the line-level culprit.

## Common mistakes

- **Optimising without measuring.** You made the cold path faster and the hot path still dominates.
- **Timing one run.** Noise swamps small differences; use `timeit.repeat` and `min`.
- **Timing with `print` inside.** Printing is slow and drowns the thing you measure.
- **`x in some_list` inside a loop.** The accidental quadratic. Convert to a `set` or `dict` before the loop.
- **Benchmarking with toy sizes.** Algorithms diverge as `n` grows; test at realistic size.

## What to take away

1. Measure before changing anything; use `perf_counter` for stopwatches and `timeit.repeat` with `min` for micro-benchmarks.
2. `set`/`dict` lookups are constant time; `list` membership scans.
3. A loop inside a loop over two tables is a quadratic join; build a dict index once and probe it.
4. Profile with `cProfile`: high `ncalls` and high `cumtime` point at the hot spot.
5. After a change, measure again to prove it helped.
