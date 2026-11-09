def downstream_models(manifest, node_id):
    children = {}
    for uid, node in manifest.get("nodes", {}).items():
        for parent in (node.get("depends_on") or {}).get("nodes", []) or []:
            children.setdefault(parent, []).append(uid)
    seen = set()
    stack = [node_id]
    while stack:
        cur = stack.pop()
        for child in children.get(cur, []):
            if child not in seen and child != node_id:
                seen.add(child)
                stack.append(child)
    return sorted(u for u in seen if u.startswith("model."))
