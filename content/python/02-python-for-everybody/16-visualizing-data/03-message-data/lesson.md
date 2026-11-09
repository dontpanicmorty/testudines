+++
id = "everybody.visualizing-data.message-data"
title = "Visualizing messages"
minutes = 30
+++

# Visualizing messages

Messages (emails, chat logs, forum posts) hold a lot of patterns: who writes the most, when people are active, which words come up. This lesson walks through the same pipeline as before, on a made-up message archive.

## Gather and clean

Imagine each message is stored with its sender and date:

```python
messages = [
    ("Ines Ward <INES@Mail.Example.org>", "2026-01-14", "Rota for the spring bird count"),
    ("omar@club.example.com",             "2026-01-30", "Re: rota for the count"),
    ("  ines@mail.example.org ",          "2026-02-02", "Binoculars for sale"),
]
```

The same person appears under three spellings: a display name, capital letters, extra spaces. Counting by these raw strings would split one sender into three. **Normalizing** means converting every variant into one standard form:

```python
def normalize(sender):
    sender = sender.strip()
    if "<" in sender and ">" in sender:
        sender = sender[sender.index("<") + 1 : sender.index(">")]
    return sender.strip().lower()

print(normalize("Ines Ward <INES@Mail.Example.org>"))   # ines@mail.example.org
print(normalize("  ines@mail.example.org "))            # ines@mail.example.org
```

Always clean *before* you count. Cleaning later is much harder, because you will have forgotten which counts to merge.

## Counting by organization

An address ends in a domain: the part after the `@`. Counting messages per domain shows which organizations are most active. You can reduce the domain to its last two labels so `mail.example.org` and `example.org` count together:

```python
def organization(address):
    domain = address.split("@")[-1]
    return ".".join(domain.split(".")[-2:])

print(organization("ines@mail.example.org"))   # example.org
```

Counting with a dictionary is the pattern you know well:

```python
counts = {}
for sender, date, subject in messages:
    org = organization(normalize(sender))
    counts[org] = counts.get(org, 0) + 1
print(counts)    # {'example.org': 2, 'example.com': 1}
```

## Counting by time period

Dates written as `YYYY-MM-DD` have a handy property: slicing off the first seven characters gives the month, `"2026-01"`. Text in that form sorts correctly in date order too.

```python
by_month = {}
for sender, date, subject in messages:
    month = date[:7]
    by_month[month] = by_month.get(month, 0) + 1
print(sorted(by_month.items()))   # [('2026-01', 2), ('2026-02', 1)]
```

A browser chart can take these pairs directly and draw a bar for each month.

## Word frequencies for a word cloud

A **word cloud** draws words in different sizes according to how often they appear. All it needs from you is a list of words and their counts. To produce one:

1. Lowercase the text and pull out the words.
2. Drop **stop words**: very common words like "the", "for", "re" that tell you nothing.
3. Count the rest and keep the top few.
4. Write them out as JSON.

```python
import re, json

stop = {"the", "for", "re", "a", "of"}
counts = {}
for sender, date, subject in messages:
    for word in re.findall(r"[a-z']+", subject.lower()):
        if word not in stop:
            counts[word] = counts.get(word, 0) + 1

top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:5]
cloud = [{"text": w, "size": n} for w, n in top]
print(json.dumps(cloud))
```

Sorting by `(-count, word)` puts the biggest first and settles ties alphabetically, so the output is always the same. A page script then scales the font size of each word using its `size`.

## Storing in between

For a large archive you would put the cleaned messages in SQLite first, and run the counts with `GROUP BY`. That way, cleaning happens once, and you can try new questions without re-reading the original files.

## Debugging tip

Spot-check by hand: pick one sender and count their messages in the raw data. If your total disagrees, look at how their address was normalized. Also print the ten rarest results; typos and odd spellings show up there.

## Common mistakes

- Counting before normalizing, so one sender is split across variants.
- Forgetting to lowercase text before counting words, so "Rota" and "rota" count separately.
- Leaving stop words in and ending up with a cloud of "the".
- Sorting only by count, which makes tied results come out in a random order.
