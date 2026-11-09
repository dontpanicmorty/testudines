def reconcile(source_ids, target_ids):
    s, t = set(source_ids), set(target_ids)
    return {"missing": sorted(s - t), "unexpected": sorted(t - s), "matched": sorted(s & t)}
