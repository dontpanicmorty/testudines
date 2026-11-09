def steps_to_one(n):
    steps = 0
    while n > 1:
        n = n // 2
        steps += 1
    return steps
