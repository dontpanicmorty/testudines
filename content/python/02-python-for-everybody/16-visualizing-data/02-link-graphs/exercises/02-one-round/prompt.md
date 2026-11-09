Write `rank_step(links, ranks, damping=0.85)` returning a **new** dictionary of scores after one round.

- `links` maps every page to the list of pages it links to. Every page appears as a key, and all targets are also keys.
- `ranks` maps every page to its current score.
- Every page starts the round with `(1 - damping) / n`, where `n` is the number of pages.
- A page with outgoing links gives `damping * rank / len(targets)` to each target.
- A page with no outgoing links gives `damping * rank / n` to every page (including itself).

Do not modify the dictionaries you were given.
