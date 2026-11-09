+++
id = "everybody.iteration.loop-patterns"
title = "Loop patterns and bisection debugging"
minutes = 25
+++

# Loop patterns and bisection debugging

Most loops you will ever write follow a few simple shapes. Learn the shapes and you can build many programs from them.

## Counting

To count how many items there are, start a counter at zero and add 1 for each item.

```python
count = 0
for item in [4, 8, 15, 16]:
    count += 1
print(count)   # 4
```

Python has `len` for this, but the pattern matters because you can count only the items you care about:

```python
big = 0
for n in [4, 80, 15, 160]:
    if n > 50:
        big += 1
print(big)   # 2
```

## Summing

Same idea, but add the item itself to a running total.

```python
total = 0
for n in [4, 8, 15, 16]:
    total += n
print(total)   # 43
```

The starting value of `0` is important. It is the "nothing added yet" state.

## Maximum and minimum

To find the largest number, remember the biggest seen so far and replace it when something larger appears. But what is "the biggest so far" before you have seen anything? Use the special value `None`, which means "no value yet".

```python
largest = None
for n in [3, 41, 12, 9]:
    if largest is None or n > largest:
        largest = n
print(largest)   # 41
```

Read the `if` carefully. On the first item `largest` is `None`, so the first part is true and we store 3. After that, we only replace it if the new number is bigger. We write `is None` (not `== None`) because that is the standard way to test for "no value".

Why not start at 0? Because if every number is negative, 0 would wrongly win. `None` works for any data. The minimum works the same way, just with `<`.

If the list is empty, `largest` stays `None`, which is an honest answer: there is no largest value.

## Filtering and searching

A loop with an `if` inside picks out the items you want.

```python
found = False
for name in ["ann", "bo", "cy"]:
    if name == "bo":
        found = True
        break
print(found)   # True
```

Setting a yes/no variable to `False` first and switching it to `True` when you see the thing is a common pattern. It is called a **flag** (a boolean variable).

## Debugging by bisection

When a long program gives wrong results, it is slow to read every line. **Bisection** means cutting the problem in half again and again.

1. Pick a point in the middle of the program and print the important variables there.
2. If they are already wrong, the bug is in the first half. If they are right, it is in the second half.
3. Repeat inside the half that holds the bug.

Ten steps of halving can pinpoint a bug among a thousand lines. The same idea works on data: if a loop fails on item 7,000, test it with the first half of the data and see.

## Common mistakes

- Starting the total at `1` or some other number by accident.
- Starting a maximum at `0` and getting the wrong answer for negative data.
- Writing `largest == None` instead of `largest is None`.
- Putting `total = 0` *inside* the loop, which resets it every time.
- Printing inside the loop when you meant to print the answer once after it.
