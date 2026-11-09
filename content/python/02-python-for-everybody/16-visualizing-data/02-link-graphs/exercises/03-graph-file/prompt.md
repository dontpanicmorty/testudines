Write `graph_json(links, rounds=20, damping=0.85)` and return a JSON **string** describing the scored network.

1. Start every page with score `1 / n`.
2. Repeat `rounds` times: every page begins with `(1 - damping) / n`, a page with links gives `damping * score / number_of_links` to each target, and a page with no links gives `damping * score / n` to every page.
3. Return `json.dumps({"nodes": [...], "links": [...]})` where nodes are `{"id": page, "rank": score_rounded_to_4_places}` sorted by id, and links are `{"source": a, "target": b}` sorted by source then target.

`links` maps each page to a list of the pages it links to; all pages appear as keys. An empty graph gives `{"nodes": [], "links": []}`.
