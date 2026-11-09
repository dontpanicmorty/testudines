def count_at_least(scores, bar):
    count = 0
    for score in scores:
        if score >= bar:
            count += 1
    return count
