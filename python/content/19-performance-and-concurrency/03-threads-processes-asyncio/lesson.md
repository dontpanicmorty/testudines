+++
id = "performance-and-concurrency.threads-processes-asyncio"
title = "Threads, processes and asyncio"
minutes = 35
+++

# Threads, processes and asyncio

You have 500 API pages to download and the loop takes ten minutes, most of it your program sitting idle waiting for the network. Or you have to hash a million files and your CPU fan is screaming on one core while the other seven do nothing. Those are two *different* problems and Python has different tools for each.

> **SQL bridge.** A warehouse runs many queries at once on separate compute. Waiting on a remote service is like a query queued behind a slow external function: the cluster is idle but the clock runs. More *concurrency* hides waiting; more *parallel compute* shortens real work. Know which one you have.

## I/O-bound versus CPU-bound

- **I/O-bound**: time is spent *waiting* (network, disk, a database). The CPU is mostly idle. Fix: overlap the waits.
- **CPU-bound**: time is spent *computing* (parsing, hashing, number-crunching). The CPU is the bottleneck. Fix: use more cores.

Diagnose first with the tools from the first lesson of this module. If the CPU is not busy while your program is slow, you are I/O-bound.

## The GIL, in practical terms

CPython has a **Global Interpreter Lock**: only one thread runs Python bytecode at a time. What this means in practice:

- Threads **do not speed up CPU-bound Python code**; they take turns.
- Threads **do speed up I/O-bound code**, because a thread waiting on I/O releases the lock and another thread runs.
- **Processes** each have their own interpreter and their own GIL, so they genuinely run in parallel, at the price of copying data between them.

| | Threads | Processes | asyncio |
|---|---|---|---|
| Good for | I/O-bound | CPU-bound | many I/O waits |
| Parallel Python code? | no (GIL) | yes | no (one thread) |
| Memory | shared | separate, data is copied | shared |
| Startup cost | tiny | large (new interpreter) | tiny |

## Threads with `concurrent.futures`

We will fake slow I/O with a tiny `time.sleep` so everything stays fast and deterministic.

```python
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_page(page: int) -> str:
    time.sleep(0.05)               # pretend: a 50 ms network call
    return f"page-{page}"

start = time.perf_counter()
serial = [fetch_page(p) for p in range(10)]
t_serial = time.perf_counter() - start

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=10) as pool:
    threaded = list(pool.map(fetch_page, range(10)))
t_threaded = time.perf_counter() - start

print(serial == threaded)                 # same results, same order
print(t_serial > 0.45, t_threaded < 0.3)  # about 10 x 50 ms versus about 50 ms
```

`pool.map` returns results **in input order** even though calls finish in any order. The `with` block waits for all work and cleans up the threads.

Use `submit` when you want individual results and per-task error handling:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def risky(n: int) -> int:
    if n == 3:
        raise ValueError("bad page 3")
    return n * 10

with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(risky, n): n for n in range(5)}
    for future in as_completed(futures):
        n = futures[future]
        try:
            print(n, future.result())     # .result() re-raises the worker's exception here
        except ValueError as exc:
            print(n, "failed:", exc)
```

Output order varies with scheduling, so never depend on `as_completed` order; map results back through the dict (or use `pool.map`).

## Processes for CPU-bound work

Same API, different executor. The function must be defined at module top level (so it can be sent to the other process), and the pool must be created under a main guard, because on macOS and Windows each worker re-imports your file.

```python
from concurrent.futures import ProcessPoolExecutor

def count_primes(limit: int) -> int:
    return sum(1 for n in range(2, limit)
               if all(n % d for d in range(2, int(n ** 0.5) + 1)))

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=2) as pool:
        print(list(pool.map(count_primes, [2000, 3000, 4000])))
```

Arguments and results are **pickled** (copied) between processes. Sending a huge DataFrame to each task costs more than the work saves; send small inputs (a file path, a range) and let the worker load its own data.

## asyncio, gently

`asyncio` achieves concurrency in **one thread** by switching tasks at every `await`. A function declared `async def` is a *coroutine*; `await` says "I'm waiting, run something else meanwhile". `asyncio.run` starts the event loop, and `asyncio.gather` runs many coroutines concurrently.

```python
import asyncio
import time

async def fetch_page(page: int) -> str:
    await asyncio.sleep(0.05)          # async-friendly sleep: yields to other tasks
    return f"page-{page}"

async def main() -> list[str]:
    return await asyncio.gather(*(fetch_page(p) for p in range(10)))

start = time.perf_counter()
pages = asyncio.run(main())
print(pages[:3], time.perf_counter() - start < 0.3)
```

Ten 50 ms waits overlap into about 50 ms. `gather` keeps results in input order.

> **Predict first.** What if `main` used a plain `for` loop with `await fetch_page(p)` inside? Each `await` finishes before the next starts, so it takes about 500 ms. Awaiting in a loop is sequential; `gather` is what makes it concurrent.

To cap concurrency (so you do not hit a rate limit), guard the work with a semaphore:

```python
import asyncio

active = 0
peak = 0

async def fetch(i: int, gate: asyncio.Semaphore) -> int:
    global active, peak
    async with gate:                   # at most 3 inside at once
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0.01)
        active -= 1
        return i

async def main() -> list[int]:
    gate = asyncio.Semaphore(3)
    return await asyncio.gather(*(fetch(i, gate) for i in range(12)))

print(asyncio.run(main()), "peak concurrency:", peak)
```

The golden rule: **never call blocking code (`time.sleep`, a blocking HTTP client, a big pandas read) inside an `async def`**. It freezes the whole event loop. Use async libraries, or hand the blocking call to a thread.

## Choosing

1. Slow because of waiting, a few dozen calls, simple code: **ThreadPoolExecutor**.
2. Thousands of concurrent waits, or you already live in async (FastAPI): **asyncio**.
3. Slow because of computing: **ProcessPoolExecutor** (or a library that releases the GIL, such as Polars and DuckDB, which already use all cores for you).
4. Not slow enough to matter: **none of the above**. Concurrency adds bugs.

## Common mistakes

- **Using threads for CPU-bound work.** No speedup, sometimes slower.
- **`await` inside a `for` loop** and wondering why nothing is concurrent. Use `gather`.
- **Blocking call inside `async def`.** The loop stalls; every other task waits.
- **Unpicklable function for a process pool**, such as a lambda or nested function: `PicklingError: Can't pickle <function <lambda>>`. Define it at module level.
- **No `if __name__ == "__main__":`** around process-pool code in a script.
- **Unbounded concurrency** against an API: you get rate-limited or banned. Cap with `max_workers` or a semaphore.
- **Shared mutable state across threads** (`counter += 1`) without a lock: lost updates. Prefer returning values.

## What to take away

1. Decide I/O-bound or CPU-bound before choosing a tool.
2. The GIL lets one thread run Python at a time: threads help I/O, processes help CPU.
3. `ThreadPoolExecutor.map` and `submit`/`as_completed` cover most I/O fan-out; `.result()` re-raises worker errors.
4. `ProcessPoolExecutor` needs top-level functions, picklable data and a main guard.
5. `asyncio.run` plus `gather` gives single-thread concurrency; awaiting in a loop is sequential.
6. Bound concurrency and never block the event loop.
