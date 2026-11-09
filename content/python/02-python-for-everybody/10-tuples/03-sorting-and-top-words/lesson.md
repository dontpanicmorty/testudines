+++
id = "everybody.tuples.sorting-and-top-words"
title = "Sorting and the most common words"
minutes = 30
+++

# Sorting and the most common words

A dictionary of counts is useful, but the question people really ask is "which items are most common?" To answer it we need to sort by **value**, and dictionaries sort by key. Tuples will help us out.

## `sorted()` versus `.sort()`

There are two ways to sort, and they behave differently.

- `my_list.sort()` sorts the list **in place** and returns `None`.
- `sorted(anything)` leaves the original alone and returns a **new list**.

```python
nums = [3, 1, 2]
print(sorted(nums))    # [1, 2, 3]
print(nums)            # [3, 1, 2]   unchanged

nums.sort()
print(nums)            # [1, 2, 3]   now changed
```

A very common bug is `nums = nums.sort()`, which stores `None`. Since tuples and strings cannot be changed, only `sorted()` works on them.

```python
print(sorted(("b", "c", "a")))    # ['a', 'b', 'c']
print(sorted("hello"))            # ['e', 'h', 'l', 'l', 'o']
```

Both accept `reverse=True` to sort from biggest to smallest.

## Sorting tuples

Since tuples compare from the left, a list of tuples sorts by the first item, then the second to break ties.

```python
pairs = [(2, "pear"), (1, "plum"), (2, "fig")]
print(sorted(pairs))
# [(1, 'plum'), (2, 'fig'), (2, 'pear')]
```

## Sorting by value: decorate, sort, undecorate

A dictionary's `.items()` pairs start with the key, so sorting them sorts by key. To sort by value we put the value first. This three-step recipe is called **decorate, sort, undecorate**:

1. **Decorate**: build a list of tuples with the thing to sort by at the front.
2. **Sort** the list.
3. **Undecorate**: pull the original data back out, if you want it.

```python
counts = {"tea": 3, "milk": 5, "rice": 3}

flipped = []
for word, n in counts.items():
    flipped.append((n, word))        # decorate: count first

flipped.sort(reverse=True)           # sort: biggest first
print(flipped)
# [(5, 'milk'), (3, 'tea'), (3, 'rice')]
```

Notice what happened to the tie: `tea` and `rice` both have 3, so the second item decides, and in reverse order `tea` comes before `rice`. If you want ties in alphabetical order, you need a trick: sort twice, or use `key=`. Here is the `key=` version, which sorts by a rule you supply:

```python
def by_count_then_word(pair):
    word, n = pair
    return (-n, word)       # negative count: biggest first; word: A to Z

print(sorted(counts.items(), key=by_count_then_word))
# [('milk', 5), ('rice', 3), ('tea', 3)]
```

A `key` function is called once on every item, and the items are ordered by what it returns. Returning a tuple lets you sort by several things at once. Putting a minus sign on a number reverses just that part.

## The top N words

To print only the 3 most common words, sort and then slice.

```python
ranked = sorted(counts.items(), key=by_count_then_word)
for word, n in ranked[:3]:
    print(word, n)
```

`ranked[:3]` means "the first three items". If there are fewer than three, you just get what exists, without an error.

## Putting it together with a file

Combine the last chapter's recipe (read, lowercase, strip punctuation, count) with sorting:

```python
import string

table = str.maketrans("", "", string.punctuation)
counts = {}
with open("notes.txt") as handle:
    for line in handle:
        for word in line.lower().translate(table).split():
            counts[word] = counts.get(word, 0) + 1

for word, n in sorted(counts.items(), key=by_count_then_word)[:5]:
    print(word, n)
```

## Debugging: sanity checks

Check that the first item is really the biggest count, and that sorting did not lose anything: `len(ranked) == len(counts)`. Test with three or four words you can count by hand, including a tie.

## Common mistakes

- `x = x.sort()` stores `None`. Use `x.sort()` alone, or `x = sorted(x)`.
- Sorting `counts.items()` without a key and expecting it to sort by count. It sorts by word.
- Forgetting `reverse=True`, so the *least* common comes first.
- Slicing with `[:n]` before sorting, which only takes the first n in dictionary order.
