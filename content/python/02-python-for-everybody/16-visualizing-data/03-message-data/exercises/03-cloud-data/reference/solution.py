import json
import re


def cloud_json(subjects, top, stop_words):
    counts = {}
    for line in subjects:
        for word in re.findall(r"[a-z']+", line.lower()):
            if word not in stop_words:
                counts[word] = counts.get(word, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:top]
    return json.dumps([{"text": w, "size": n} for w, n in ordered])
