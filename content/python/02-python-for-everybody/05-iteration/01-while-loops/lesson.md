+++
id = "everybody.iteration.while-loops"
title = "Repeating with while"
minutes = 20
+++

# Repeating with while

Computers are good at doing the same thing many times without getting bored. A piece of code that repeats is called a **loop**. In this lesson you meet the `while` loop, which keeps repeating for as long as a question has the answer `True`.

## Updating a variable

Before loops make sense, you need to be comfortable changing a variable using its own old value.

```python
coins = 5
coins = coins + 1
print(coins)   # 6
```

Read the second line from right to left: take the current value of `coins`, add 1, and store the result back in `coins`. Python lets you write the same thing shorter as `coins += 1`.

Two names are worth knowing:

- **Initializing** a variable means giving it its first value (`coins = 5`). Using a variable that has no value yet is an error.
- **Incrementing** means adding to it (usually 1). **Decrementing** means subtracting.

```python
countdown = 3
countdown -= 1   # now 2
```

## The while statement

A `while` loop checks a condition. If it is `True`, Python runs the indented block, then checks again. When the condition is `False`, the loop ends and Python moves on.

```python
n = 3
while n > 0:
    print(n)
    n = n - 1
print("Lift off")
```

This prints `3`, `2`, `1` and then `Lift off`. Each trip through the block is called an **iteration**.

The variable `n` here is the **iteration variable**: it changes each time round and eventually makes the condition false. If nothing inside the loop ever changes it, you get a problem.

## Infinite loops

```python
n = 3
while n > 0:
    print(n)      # forgot to change n!
```

The condition is always `True`, so this prints `3` forever. That is an **infinite loop**. If you ever start one by accident, stop it with Ctrl+C in a terminal. Always ask yourself: what inside the loop makes the condition become false?

## Finishing early with break

Sometimes you only know it is time to stop in the middle of the block. The `break` statement jumps straight out of the loop.

```python
total = 0
while True:
    total += 10
    if total >= 35:
        break
print(total)   # 40
```

`while True:` looks scary but it is fine as long as a `break` can happen. It is a handy way to say "keep going until I say stop".

## Skipping with continue

The `continue` statement skips the rest of the current iteration and jumps back to the top to check the condition again.

```python
n = 0
while n < 6:
    n += 1
    if n % 2 == 0:
        continue      # skip even numbers
    print(n)
```

This prints `1`, `3`, `5`. Note that `n += 1` comes *before* the `continue`. If it came after, the loop would get stuck on an even number forever.

## Common mistakes

- Forgetting to update the iteration variable, which causes an infinite loop.
- Updating it in the wrong direction (adding when you meant to subtract).
- Using `continue` before the line that updates the variable.
- Starting with a condition that is already `False`, so the loop never runs at all. That is legal, just surprising.
- Being off by one: `n > 0` and `n >= 0` give different numbers of iterations.
