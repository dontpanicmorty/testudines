+++
id = "iteration-and-idioms.generators-and-lazy-data"
title = "Generators and lazy data"
minutes = 30
+++

# Generators and lazy data

A warehouse never loads a 50 GB table into your laptop's memory to filter it; it streams. Python's **iterators** and **generators** give you the same ability: process data one row at a time, so memory stays flat no matter how big the input is. This is the foundation of every scalable pipeline you'll write.

> **SQL bridge.** A database cursor: you `FETCH` rows as you need them and the result set is never fully materialised. A generator is a cursor you write yourself.

## Iterables and iterators

Anything you can `for`-loop over is an **iterable**. Calling `iter()` on it gives an **iterator**, an object that hands out the next item each time you call `next()` and raises `StopIteration` when done.

```python
it = iter(["a", "b"])
print(next(it))
print(next(it))
print(next(it, "done"))    # a default avoids StopIteration
```

A `for` loop is just a `next()` loop that stops quietly. Importantly, **an iterator is single-use**: once consumed it's empty.

```python
nums = iter([1, 2, 3])
print(sum(nums))
print(sum(nums))   # already used up
```

> **Predict first.** What does the second `sum` print? `0`. Reusing an exhausted iterator is a classic "my data vanished" bug. A list can be iterated many times; an iterator once.

## Generator functions and yield

Write a function with `yield` instead of `return` and calling it gives you a generator (a lazy iterator). The body runs only as items are requested, pausing at each `yield`.

```python
def countdown(n):
    print("starting")
    while n > 0:
        yield n
        n -= 1
    print("finished")

gen = countdown(3)
print("created, nothing has run yet")
print(next(gen))
print(list(gen))
```

Notice "starting" appears only on the first `next`. Calling `countdown(3)` did no work. This laziness is the entire point.

## Generator expressions

A comprehension with parentheses instead of brackets is lazy:

```python
squares_list = [n * n for n in range(5)]   # built now, held in memory
squares_gen = (n * n for n in range(5))    # computed on demand

print(squares_list)
print(squares_gen)
print(sum(squares_gen))
```

When the only consumer is `sum`, `max`, `any`, `all`, `sorted` or a `for` loop, use a generator expression: `sum(o["amount"] for o in orders)` never builds an intermediate list.

## Streaming a file row by row

Open files are lazy iterators over lines. This is how you process a file bigger than memory:

```python
import csv, io

fake_file = io.StringIO("id,amount\n1,10.5\n2,\n3,7.25\n")   # stands in for open("orders.csv")

def read_amounts(f):
    for row in csv.DictReader(f):       # one row at a time
        if row["amount"]:
            yield int(row["id"]), float(row["amount"])

for order_id, amount in read_amounts(fake_file):
    print(order_id, amount)
```

Real code is the same with `with open(path, newline="") as f:` in place of the `StringIO`. Compare the naive version, `rows = list(csv.DictReader(f))`, which loads **everything** first.

## Pipelines of generators

Each stage takes an iterable and yields an iterable, so stages compose like `SELECT … FROM (SELECT … FROM (…))`:

```python
def parse(lines):
    for line in lines:
        order_id, amount = line.split(",")
        yield {"id": order_id, "amount": float(amount)}

def only_big(rows, threshold):
    for r in rows:
        if r["amount"] >= threshold:
            yield r

lines = ["a,5.0", "b,50.0", "c,500.0"]
pipeline = only_big(parse(lines), 10)
print(list(pipeline))
```

Rows flow through the whole chain one at a time. Nothing is held between stages, and an early `break` (or `next(...)`) stops upstream work too.

## itertools basics

The standard library ships lazy building blocks:

```python
from itertools import islice, chain, count, groupby

print(list(islice(count(1), 5)))                    # first 5 of an infinite stream
print(list(chain([1, 2], [3], [4, 5])))             # concatenate iterables lazily
print(list(islice(range(100), 10, 13)))             # slice without building a list

events = [("eu", 1), ("eu", 2), ("us", 3)]
for region, grp in groupby(events, key=lambda e: e[0]):   # input must already be sorted by key
    print(region, [v for _, v in grp])
```

`groupby` only groups **adjacent** items, so sort first (or use `defaultdict`). For batching rows into chunks, `islice` in a loop is the building block you'll use for bulk inserts.

```python
from itertools import islice

def batches(iterable, size):
    it = iter(iterable)
    while chunk := list(islice(it, size)):
        yield chunk

print(list(batches(range(7), 3)))
```

## Why laziness matters

- **Memory:** constant, not proportional to the input size.
- **Latency:** the first result appears immediately, so you can stop early after finding what you need.
- **Composability:** infinite or unknown-length sources (paged APIs, log tails) become ordinary loops.
- **Cost:** a generator you never finish never does the remaining work.

The price is that generators are single-use and you cannot ask for `len()` or index them. If you need either, `list(gen)` once and keep the list.

## Common mistakes

- Consuming a generator twice, then wondering why the second pass is empty.
- `TypeError: object of type 'generator' has no len()`: materialise with `list(...)` or count as you go.
- `TypeError: 'generator' object is not subscriptable`: use `itertools.islice` instead of `gen[0:5]`.
- Putting `return value` in a loop-style generator when you meant `yield value`.
- Closing the file before the generator is consumed (`ValueError: I/O operation on closed file`): keep the `with open(...)` around the consuming loop, or put the `with` **inside** the generator.

## What to take away

1. Iterators produce items on demand and are single-use.
2. `yield` turns a function into a lazy generator; nothing runs until you ask.
3. `(expr for x in xs)` is a lazy comprehension; pass it straight into `sum`, `max`, `any`.
4. Stream files with `for line in f` / `csv.DictReader`; chain generators into pipelines.
5. `islice`, `chain`, `groupby` cover most needs; materialise with `list()` only when you must.
