def summarize(numbers):
    count = 0
    total = 0
    largest = None
    for n in numbers:
        count += 1
        total += n
        if largest is None or n > largest:
            largest = n
    return {"count": count, "total": total, "largest": largest}
