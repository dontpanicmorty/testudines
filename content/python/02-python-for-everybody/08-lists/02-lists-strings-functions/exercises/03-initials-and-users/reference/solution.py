def senders(lines):
    users = []
    for line in lines:
        if not line.startswith("From: "):
            continue
        address = line.split()[1]
        user = address.split("@")[0]
        if user not in users:
            users.append(user)
    users.sort()
    return users
