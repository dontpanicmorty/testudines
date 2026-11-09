def months_to_reach(goal, deposit, percent):
    balance = 0
    months = 0
    while balance < goal:
        balance += deposit
        balance += balance * percent / 100
        months += 1
    return months
