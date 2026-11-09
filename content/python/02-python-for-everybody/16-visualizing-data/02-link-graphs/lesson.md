+++
id = "everybody.visualizing-data.link-graphs"
title = "Networks and link scores"
minutes = 30
+++

# Networks and link scores

Some data is about *connections* more than values: which page links to which, who writes to whom, which station feeds which route. A set of items with links between them is called a **graph**. The items are **nodes** and the links are **edges**.

## A link graph from pages

Imagine a tiny website of three pages. Each page's HTML contains links to others:

```python
pages = {
    "home.html":  '<a href="news.html">News</a> <a href="about.html">About</a>',
    "news.html":  '<a href="home.html">Home</a>',
    "about.html": '<a href="home.html">Home</a> <a href="news.html">News</a> <a href="https://elsewhere.test/">Away</a>',
}
```

To build the graph, collect for each page the set of pages it points to. You already know how to pull `href` values out of HTML with a regular expression or BeautifulSoup. We only keep links to pages **we know about**, to keep the graph inside our site:

```python
import re

def outgoing(html, known):
    hrefs = re.findall(r'href="([^"]+)"', html)
    return sorted({h for h in hrefs if h in known})

links = {name: outgoing(html, pages) for name, html in pages.items()}
print(links)
# {'home.html': ['about.html', 'news.html'], 'news.html': ['home.html'],
#  'about.html': ['home.html', 'news.html']}
```

The graph is stored as a dictionary: each node maps to the list of nodes it links *to*. Using a set while collecting removes duplicate links.

## Which page matters most?

A page that many pages link to seems important. And a link from an important page counts for more than a link from an obscure one. Search engines turn that idea into a score. Here is a simple version in the PageRank style, built from one rule:

> Each page splits its current score equally among the pages it links to.

Start every page with the same score (1 divided by the number of pages). Then repeat: each page's new score is made of what it receives from the pages that link to it.

```python
def step(links, ranks, damping=0.85):
    n = len(links)
    new = {page: (1 - damping) / n for page in links}
    for page, targets in links.items():
        if targets:
            share = ranks[page] / len(targets)
            for t in targets:
                new[t] += damping * share
        else:
            # a page with no links hands its score to everyone equally
            for p in new:
                new[p] += damping * ranks[page] / n
    return new
```

The **damping** factor (commonly 0.85) models a reader who sometimes gets bored and jumps to a random page. It also keeps the scores from getting stuck. The `(1 - damping) / n` part is every page's guaranteed small base score.

Notice the total of all scores stays 1 after each step, so the scores behave like shares of attention.

## Iterating until it settles

One step is not enough, because scores received depend on scores that are themselves changing. Repeat the step and watch the scores stop moving:

```python
ranks = {p: 1 / len(links) for p in links}
for _ in range(20):
    ranks = step(links, ranks)

for page, score in sorted(ranks.items(), key=lambda kv: -kv[1]):
    print(f"{page}: {score:.3f}")
```

After a couple of dozen rounds the numbers change in only the fourth decimal place or so. We say the score has **converged**. A fixed number of iterations is simple and works well for small graphs.

## Exporting nodes and links as JSON

To draw the network in a browser (for example with a force-directed layout in a JavaScript library), you give the page two lists: nodes and links.

```python
import json

graph = {
    "nodes": [{"id": p, "rank": round(ranks[p], 4)} for p in sorted(ranks)],
    "links": [{"source": a, "target": b} for a in sorted(links) for b in links[a]],
}
text = json.dumps(graph)
```

A browser-side script reads this file and draws a circle per node, larger for a higher `rank`, and a line per link. You produce data and the page draws it.

## Debugging tip

Check the **sum** of the scores. If it drifts away from 1, you lost or double-counted a page, often a page with no outgoing links. Also try a graph of two pages that link to each other: both scores should be exactly equal.

## Common mistakes

- Dividing a page's score by the number of pages instead of by its number of outgoing links.
- Counting duplicate links twice. Collect them into a set first.
- Forgetting pages with no outgoing links, who are missing from the sums.
- Updating scores in place while still reading the old ones. Build a **new** dictionary each round.
